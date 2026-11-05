## 1D Register Tiling: One Thread, TM Outputs

Kernel 4 moved the traffic instead of removing it. Global loads per output element fell 32 times, runtime fell 1.41 times, and the count that did not move at all was the shared memory one: `2K` = 8192 reads per output element, one from `As` and one from `Bs` for every multiply accumulate. We swapped a load that crosses the memory bus for a roughly 33 cycle shared memory load[^1], and kept the number of loads identical.

The reason that count is stuck is the thread mapping, not the memory. One thread owns one element of C, so every value it pulls out of shared memory feeds exactly one FMA and is then discarded. There is no way to amortize a load across arithmetic when there is only one piece of arithmetic to amortize it against.

So give a thread more than one output. Let one thread own a short column of C, `TM` elements tall, all in the same column and in consecutive rows. Those `TM` outputs all need the same element of B, because they share a column, and they need `TM` different elements of A. The thread loads the B value once into a register and multiplies it against `TM` values of A. One shared memory read now feeds `TM` FMAs instead of one.

![One block owns a 64 x 64 tile of C walked in steps of BK = 8, and one thread now owns a column of 8 consecutive cells instead of a single cell.](/images/gemm/register-1d-overview.png "full")

That is the whole idea, and the accounting for it is immediate. Per step of the K loop a thread reads `1` value of B and `TM` values of A, so `1 + TM` reads produce `TM` results instead of `2` reads producing `1`.

![One step of the BK loop, where a single Bs value is read into the register regN and reused across TM = 8 values of As, feeding 8 accumulators.](/images/gemm/register-1d-inner-loop.png "large")

### The Kernel

The tile shape changes along with the thread mapping. The block now owns a `64 x 64` tile of C and walks K in steps of `BK = 8`, and because each thread produces `TM = 8` outputs the block needs `(64 x 64) / 8 = 512` threads rather than 4096:

```cuda
const int BM = 64, BN = 64, BK = 8, TM = 8;

dim3 gridDim(CEIL_DIV(N, BN), CEIL_DIV(M, BM));
dim3 blockDim((BM * BN) / TM);   // 512

sgemm_register_tiling_1d<BM, BN, BK, TM><<<gridDim, blockDim>>>(M, N, K, alpha, A, B, beta, C);
```

```cuda
// Block tile is BM x BN of C, walked over K in chunks of BK.
// Thread count = (BM * BN) / TM.
template <const int BM, const int BN, const int BK, const int TM>
__global__ void sgemm_register_tiling_1d(int M, int N, int K, float alpha, const float *A, const float *B, float beta, float *C) {
  // blockIdx.x indexes columns so that consecutive blocks share the same rows
  // of A -- better L2 hit rate than the .x=row mapping in kernel 3.
  const int cRow = blockIdx.y;
  const int cCol = blockIdx.x;

  __shared__ float As[BM * BK];
  __shared__ float Bs[BK * BN];

  // position of this thread within the BM x BN output tile.
  // threadRow is the *tile* row: this thread owns rows
  // [threadRow*TM, threadRow*TM + TM) of the block tile.
  const int threadCol = threadIdx.x % BN;
  const int threadRow = threadIdx.x / BN;

  // move the pointers to the start of this block's work
  A += cRow * BM * K;                   // row = cRow, col = 0
  B += cCol * BN;                       // row = 0,    col = cCol
  C += cRow * BM * N + cCol * BN;       // row = cRow, col = cCol

  // Determine where the thread loads the tiles A and B in SMEM 
  const int innerColA = threadIdx.x % BK;  // 0..BK-1
  const int innerRowA = threadIdx.x / BK;  // 0..BM-1
                                           //
  const int innerColB = threadIdx.x % BN;  // 0..BN-1
  const int innerRowB = threadIdx.x / BN;  // 0..BK-1

  // per-thread accumulators, live in registers
  float threadResults[TM] = {0.0f};

  for (int bkIdx = 0; bkIdx < K; bkIdx += BK) {
    // populate the SMEM caches
    As[innerRowA * BK + innerColA] = A[innerRowA * K + innerColA];
    Bs[innerRowB * BN + innerColB] = B[innerRowB * N + innerColB];
    __syncthreads();

    // advance onto the next chunk along K
    A += BK;
    B += BK * N;

    // compute the per-thread partial results out of SMEM
    for (int dotIdx = 0; dotIdx < BK; ++dotIdx) {
      // one B value, hoisted into a register and reused TM times below
      float regN = Bs[dotIdx * BN + threadCol];
      for (int resIdx = 0; resIdx < TM; ++resIdx) {
        threadResults[resIdx] += As[(threadRow * TM + resIdx) * BK + dotIdx] * regN;
      }
    }
    __syncthreads();
  }

  // write out the TM results owned by this thread
  for (int resIdx = 0; resIdx < TM; ++resIdx) {
    C[(threadRow * TM + resIdx) * N + threadCol] =
        alpha * threadResults[resIdx] +
        beta * C[(threadRow * TM + resIdx) * N + threadCol];
  }
}
```

### Mechanics

1. **One hoisted line is the entire kernel.** `float regN = Bs[dotIdx * BN + threadCol];` sits outside the `resIdx` loop, so the B value is read once and reused `TM` times from a register. Move that line inside the inner loop and you have written kernel 4 again with extra steps: same results, same arithmetic, eight times the shared memory reads. Everything else in this file is bookkeeping to make that hoist possible.

2. **The same 512 threads are decomposed two different ways.** For loading, `innerRowA`/`innerColA` cut the block into a `64 x 8` grid matching the shape of the A tile, and `innerRowB`/`innerColB` cut it into `8 x 64` matching the B tile. For computing, `threadRow`/`threadCol` cut it into `8 x 64`, where the row index is scaled by `TM` on use. This is what kernel 3 was for. None of these three shapes is the launch shape, and all three come out of the same flat `threadIdx.x`.

3. **The loads still land exactly, with no loop.** `As` holds `BM x BK = 512` floats and `Bs` holds `BK x BN = 512`, and there are 512 threads, so each thread copies one element of each and the load is a single statement. This is a coincidence of the chosen tile shape, not a property of the technique, and the next kernel loses it.

4. **`threadRow * TM + resIdx`, not `threadRow + resIdx * something`.** A thread's `TM` outputs are consecutive rows, so its rows are `threadRow * TM` through `threadRow * TM + TM - 1`. That keeps `threadCol` as the fast moving index across a warp, which keeps the store to C coalesced. The read from `As` marches down a column of the tile with a stride of `BK`, which shared memory does not mind the way global memory would.

Kernel 5 runs in **10.506 ms at 13081.8 GFLOP/s, which is 36.3% of cuBLAS at `M = N = K = 4096`**, up from 33.268 ms and 11.5%. That is 3.17 times faster than kernel 4, and the largest single jump in the series.

### The Arithmetic

Global memory first, because the tile grew. `K x (1/BM + 1/BN)` with `BM = BN = 64` gives `K / 32 = 128` loads per output element, down from 256, so doubling each tile dimension halved global traffic to **8.59 GB**. That is a real improvement and it is not where the speedup came from.

Shared memory is where the section lives. Per step of the K loop a thread now issues `1 + TM = 9` reads to produce `TM = 8` results, so:

```
SMEM accesses per result = K * (1 + TM) / TM
                         = 4096 * 9 / 8
                         = 4608
```

against `2K = 8192` for kernel 4. That is a factor of **1.78**, and the runtime moved by a factor of **3.17**. The count under-predicts the win by nearly twice, which is worth stopping on because it is the opposite of kernel 4's problem, where the count over-predicted.

The reason is that a shared memory read is not only a latency to be hidden, it is an instruction to be issued. Kernel 4's inner loop issued two `LDS` and one `FFMA` per output; this one issues nine `LDS` and eight `FFMA` per eight outputs. The loads that disappeared took issue slots with them, and the ratio of memory instructions to arithmetic instructions went from 2:1 to 9:8. Access counts measure bytes touched. They do not measure the instruction stream, and from here on the instruction stream is increasingly what we are fighting.

Nsight measures that shift directly. Kernel 4 sat at 40.5 warp cycles per issued instruction with 23.9 of them, 58.9%, stalled on `Stall MIO Throttle`, the queue a warp waits in for a shared memory instruction to issue. This kernel runs at **21.0 warp cycles per issued instruction with MIO throttle down to 6.6 cycles, 31.4%**. The stall did not merely shrink in proportion to the loads removed; the whole issue pipeline got shorter.

The occupancy table says the same thing from another direction. This kernel uses 48 registers per thread against kernel 4's 40, and at 512 threads per block that is 2 blocks per SM and 66.7% occupancy, identical to kernel 4's. We bought an extra 8 registers per thread and paid nothing for them.

### What Could Be Improved

The reuse is one sided. A thread reads a value of A once and uses it once; it reads a value of B once and uses it `TM` times. Written as a ratio, `1 + TM` loads feed `TM` FMAs, so as `TM` grows the loads per FMA approach 1 and stop there. Even at `TM = 64` every FMA would still cost roughly one shared memory read, because the A side never amortizes at all.

The fix is symmetric with the problem. A thread owns a column of C, which is why only B is shared among its outputs. Give it a rectangle instead and both operands amortize at once.

[^1]: [Dissecting the SM_120 Microarchitecture: Cycle-Level Characterization of Blackwell Consumer GPUs](https://zartbot.github.io/micro_arch/nvidia/sm_120/paper.html)
