import { ImageResponse } from "next/og";
import { defaultDescription, siteName } from "@/lib/metadata";

export const alt = siteName;
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

async function loadNewsreader(text: string) {
  // Fetch only the glyphs we need so the serif title matches the site.
  const url = `https://fonts.googleapis.com/css2?family=Newsreader:wght@400&text=${encodeURIComponent(text)}`;
  const css = await fetch(url, {
    headers: {
      // A browser UA makes Google return woff2 (which next/og can't use);
      // an older UA returns a TrueType .ttf that ImageResponse supports.
      "User-Agent":
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8) AppleWebKit/534.30",
    },
  }).then((res) => res.text());

  const fontUrl = css.match(/src: url\((.+?)\) format\('(opentype|truetype)'\)/)?.[1];
  if (!fontUrl) return null;

  return fetch(fontUrl).then((res) => res.arrayBuffer());
}

export default async function Image() {
  const fontData = await loadNewsreader(`${siteName}${defaultDescription}`).catch(
    () => null
  );

  return new ImageResponse(
    (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          backgroundColor: "#ffffff",
          padding: "80px",
        }}
      >
        <div
          style={{
            display: "flex",
            fontSize: 96,
            lineHeight: 1.1,
            letterSpacing: "-0.02em",
            color: "#0a0a0a",
            fontFamily: fontData ? "Newsreader" : "serif",
          }}
        >
          {siteName}
        </div>
        <div
          style={{
            display: "flex",
            marginTop: 32,
            fontSize: 36,
            lineHeight: 1.4,
            color: "#525252",
            fontFamily: fontData ? "Newsreader" : "serif",
          }}
        >
          {defaultDescription}
        </div>
      </div>
    ),
    {
      ...size,
      fonts: fontData
        ? [{ name: "Newsreader", data: fontData, style: "normal", weight: 400 }]
        : [],
    }
  );
}
