import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: "/essays/:year/:slug",
        destination: "/essays/:slug",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
