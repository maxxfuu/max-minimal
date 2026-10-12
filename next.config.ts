import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: "/essays/:year(\\d{4})/:slug",
        destination: "/writings/:slug",
        permanent: true,
      },
      {
        source: "/essays",
        destination: "/writings",
        permanent: true,
      },
      {
        source: "/essays/:path*",
        destination: "/writings/:path*",
        permanent: true,
      },
      // The CUDA hardware primer was split out of the GEMM series as its own
      // essay (article4), which pushed the series to article5 and the attention
      // essay to article6. Keep the old URLs working.
      {
        source: "/writings/article5",
        destination: "/writings/article6",
        permanent: true,
      },
      {
        source: "/writings/article4/page1",
        destination: "/writings/article5/page1",
        permanent: true,
      },
      {
        source: "/writings/article4/page2",
        destination: "/writings/article4",
        permanent: true,
      },
      ...Array.from({ length: 13 }, (_, i) => ({
        source: `/writings/article4/page${i + 3}`,
        destination: `/writings/article5/page${i + 2}`,
        permanent: true,
      })),
    ];
  },
};

export default nextConfig;
