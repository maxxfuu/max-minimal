import type { Metadata } from "next";

export const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://maxxfuu.com";
export const siteName = "Max Fu";
export const defaultDescription =
  "Software engineer, entrepreneur, and student.";

const defaultOgImage = {
  url: "/favicon.ico",
  width: 1200,
  height: 630,
  alt: siteName,
};

export function createPageMetadata({
  title,
  description = defaultDescription,
  path = "/",
  type = "website",
  // When true, omit the explicit favicon image so a file-based
  // `opengraph-image` route can supply a dynamically generated image.
  dynamicImage = false,
}: {
  title: string;
  description?: string;
  path?: string;
  type?: "website" | "article";
  dynamicImage?: boolean;
}): Metadata {
  const url = `${siteUrl}${path}`;
  const pageTitle = path === "/" ? title : `${title} · ${siteName}`;

  return {
    title: pageTitle,
    description,
    alternates: {
      canonical: url,
    },
    openGraph: {
      title,
      description,
      url,
      siteName,
      locale: "en_US",
      type,
      ...(dynamicImage ? {} : { images: [defaultOgImage] }),
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      ...(dynamicImage ? {} : { images: [defaultOgImage.url] }),
    },
  };
}

export const rootMetadata: Metadata = {
  metadataBase: new URL(siteUrl),
  icons: {
    icon: "/favicon.ico",
  },
  ...createPageMetadata({
    title: siteName,
    description: defaultDescription,
    path: "/",
  }),
};
