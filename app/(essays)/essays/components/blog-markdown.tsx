import type { ReactNode } from "react";
import { Fragment } from "react";

function renderInlineMarkdown(text: string) {
  const parts = text.split(/(`[^`]+`)/g);

  return parts.map((part, index) => {
    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={`${part}-${index}`}
          className="font-mono text-[0.9em] text-muted-foreground"
        >
          {part.slice(1, -1)}
        </code>
      );
    }

    return <Fragment key={`${part}-${index}`}>{part}</Fragment>;
  });
}

function normalizeHeading(text: string) {
  return text.trim().toLowerCase();
}

interface BlogMarkdownProps {
  body: string;
  title?: string;
}

export function BlogMarkdown({ body, title }: BlogMarkdownProps) {
  const lines = body.split("\n");
  const elements: ReactNode[] = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];

    if (!line.trim()) {
      index += 1;
      continue;
    }

    if (line.startsWith("```")) {
      const language = line.slice(3).trim() || "text";
      const codeLines: string[] = [];
      index += 1;

      while (index < lines.length && !lines[index].startsWith("```")) {
        codeLines.push(lines[index]);
        index += 1;
      }

      elements.push(
        <pre
          key={`code-${index}`}
          className="my-10 overflow-x-auto border-y border-border py-6 font-mono text-sm leading-relaxed text-foreground"
        >
          <div className="mb-3 font-sans text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
            {language}
          </div>
          <code>{codeLines.join("\n")}</code>
        </pre>
      );

      index += 1;
      continue;
    }

    const headingMatch = line.match(/^(#{1,3})\s+(.*)$/);

    if (headingMatch) {
      const [, hashes, headingText] = headingMatch;
      const level = hashes.length;

      if (
        level === 1 &&
        title &&
        normalizeHeading(headingText) === normalizeHeading(title)
      ) {
        index += 1;
        continue;
      }

      if (level === 1) {
        elements.push(
          <h2
            key={`h2-${index}`}
            className="mt-16 mb-6 text-2xl font-normal tracking-tight text-foreground md:text-3xl"
          >
            {renderInlineMarkdown(headingText)}
          </h2>
        );
      } else if (level === 2) {
        elements.push(
          <h3
            key={`h3-${index}`}
            className="mt-12 mb-4 text-xl font-normal tracking-tight text-foreground md:text-2xl"
          >
            {renderInlineMarkdown(headingText)}
          </h3>
        );
      } else {
        elements.push(
          <h4
            key={`h4-${index}`}
            className="mt-10 mb-3 text-lg font-normal tracking-tight text-foreground"
          >
            {renderInlineMarkdown(headingText)}
          </h4>
        );
      }

      index += 1;
      continue;
    }

    if (line.startsWith("> ") || line === ">") {
      const calloutLines: string[] = [];

      while (index < lines.length && (lines[index].startsWith("> ") || lines[index] === ">")) {
        calloutLines.push(lines[index].replace(/^>\s?/, ""));
        index += 1;
      }

      elements.push(
        <aside
          key={`callout-${index}`}
          className="my-10 border-l-2 border-foreground/20 bg-muted/50 px-5 py-4 text-[0.98rem] leading-[1.85] text-muted-foreground"
        >
          {renderInlineMarkdown(calloutLines.join(" "))}
        </aside>
      );

      continue;
    }

    const mediaMatch = line.trim().match(/^!\[([^\]]*)\]\(([^)\s]+)\)$/);

    if (mediaMatch) {
      const [, caption, src] = mediaMatch;
      const isVideo = /\.(mp4|webm|mov)$/i.test(src);

      elements.push(
        <figure key={`media-${index}`} className="my-10">
          {isVideo ? (
            <video
              src={src}
              autoPlay
              loop
              muted
              playsInline
              className="w-full rounded-md border border-border"
            />
          ) : (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={src}
              alt={caption}
              className="w-full rounded-md border border-border"
            />
          )}
          {caption ? (
            <figcaption className="mt-3 text-center font-sans text-xs text-muted-foreground">
              {caption}
            </figcaption>
          ) : null}
        </figure>
      );

      index += 1;
      continue;
    }

    if (line.startsWith("- ")) {
      const items: string[] = [];

      while (index < lines.length && lines[index].startsWith("- ")) {
        items.push(lines[index].slice(2));
        index += 1;
      }

      elements.push(
        <ul
          key={`list-${index}`}
          className="my-8 ml-5 list-disc space-y-3 text-base leading-[1.85] text-foreground"
        >
          {items.map((item, itemIndex) => (
            <li key={`${item}-${itemIndex}`}>{renderInlineMarkdown(item)}</li>
          ))}
        </ul>
      );

      continue;
    }

    const paragraphLines = [line];
    index += 1;

    while (
      index < lines.length &&
      lines[index].trim() &&
      !lines[index].match(/^#{1,3}\s+/) &&
      !lines[index].startsWith("> ") &&
      lines[index] !== ">" &&
      !lines[index].startsWith("- ") &&
      !lines[index].startsWith("```") &&
      !lines[index].trim().startsWith("![")
    ) {
      paragraphLines.push(lines[index]);
      index += 1;
    }

    elements.push(
      <p
        key={`p-${index}`}
        className="text-base leading-[1.85] text-foreground md:text-[1.05rem]"
      >
        {renderInlineMarkdown(paragraphLines.join(" "))}
      </p>
    );
  }

  return <div className="space-y-6">{elements}</div>;
}
