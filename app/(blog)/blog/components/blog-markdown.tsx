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

export function BlogMarkdown({ body }: { body: string }) {
  const lines = body.split("\n");
  const elements: ReactNode[] = [];
  let index = 0;
  let skippedTitle = false;

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

    if (line.startsWith("## ")) {
      elements.push(
        <h2
          key={`h2-${index}`}
          className="mt-16 mb-6 text-xl font-normal lowercase tracking-tight text-foreground md:text-2xl"
        >
          {renderInlineMarkdown(line.slice(3).toLowerCase())}
        </h2>
      );
      index += 1;
      continue;
    }

    if (line.startsWith("# ")) {
      if (!skippedTitle) {
        skippedTitle = true;
        index += 1;
        continue;
      }

      elements.push(
        <h2
          key={`h1-${index}`}
          className="mt-16 mb-6 text-2xl font-normal lowercase tracking-tight md:text-3xl"
        >
          {renderInlineMarkdown(line.slice(2).toLowerCase())}
        </h2>
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
      !lines[index].startsWith("#") &&
      !lines[index].startsWith("- ") &&
      !lines[index].startsWith("```")
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
