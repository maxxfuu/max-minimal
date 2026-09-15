# Excalidraw sources for the hand-drawn figures

Editable `.excalidraw` sources for every hand-drawn figure in the essays: the
GEMM article in `content/essays/article4/`, one directory per page, plus one
directory per standalone essay.

The `article5/` scenes were authored here from the start, so the generator is
the source of truth for them. For the GEMM figures it is the other way round:
the original scenes were not recoverable — the exported PNGs in
`public/images/gemm/` carry no embedded scene data, and the local Excalidraw
app's storage held only an empty canvas. Each scene here was rebuilt from the
exported PNG and then checked by rendering it back through Excalidraw's own
export pipeline and comparing against the original.

## Layout

| directory | figures | referenced by |
|---|---|---|
| `page2/` | 9 | `page2.md` |
| `page3/` | 3 | `page3.md` |
| `page4/` | 3 | `page4.md` |
| `page6/` | 3 | `page6.md` |
| `page7/` | 2 | `page7.md` |
| `page8/` | 1 | `page8.md` |
| `article5/` | 3 | `article5.md` |

Each file is named after the PNG it reproduces, so
`page2/memory-hierarchy.excalidraw` corresponds to
`public/images/gemm/memory-hierarchy.png`, and
`article5/tokenization.excalidraw` to
`public/images/attention/tokenization.png`.

`page1.md` has no directory: its only image, `kernel-benchmark.png`, is a
`gnome-screenshot` of terminal output, not an Excalidraw drawing.

`_preview/` holds a PNG render of every scene in this tree, for diffing against
the published PNGs under `public/images/`.

## Editing

Open any `.excalidraw` file in the local Excalidraw app (File → Open) or at
excalidraw.com. To re-export a figure, use File → Export image → PNG with
background on, and overwrite the matching file under `public/images/`. The
preview render that `build_all.sh` writes is the same export, so copying it out
of `_preview/` works too.

## Regenerating

The scenes are emitted by the Python generators in `_generators/`, one per
figure, on top of the small builder library `_generators/exc.py`. Editing a
generator and re-running it is usually easier than nudging elements by hand.

```sh
cd _generators
python3 page2_memory_hierarchy.py      # rewrite one scene
./build_all.sh                         # rewrite all scenes and re-render previews
```

`build_all.sh` also runs `harness/`, which measures every text element with the
real Excalifont/Cascadia metrics, writes the correct `width`/`height` and
anchor-resolved `x`/`y` back into the scene, and renders a preview PNG. See
`harness/run.sh` for its one-time setup (it needs `npm install` plus a local
static server on port 8787).

Note that Excalidraw's sketchy rendering is seeded per element, so a rebuilt
scene is geometrically identical but the individual pen strokes will differ
slightly from the original export.
