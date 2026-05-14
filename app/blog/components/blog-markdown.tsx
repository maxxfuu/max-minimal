import type { ReactNode } from "react";
import { Fragment } from "react";

function renderInlineMarkdown(text: string) {
  const parts = text.split(/(`[^`]+`)/g);

  return parts.map((part, index) => {
    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={`${part}-${index}`}
          className="rounded bg-neutral-100 px-1.5 py-0.5 font-mono text-[0.9em] dark:bg-neutral-900"
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
          className="overflow-x-auto rounded-2xl border border-neutral-200 bg-neutral-950 p-4 text-sm text-neutral-100 dark:border-neutral-800"
        >
          <div className="mb-3 text-xs uppercase tracking-[0.2em] text-neutral-400">
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
        <h2 key={`h2-${index}`} className="mt-10 text-2xl font-semibold">
          {renderInlineMarkdown(line.slice(3))}
        </h2>
      );
      index += 1;
      continue;
    }

    if (line.startsWith("# ")) {
      elements.push(
        <h1 key={`h1-${index}`} className="mt-6 text-3xl font-semibold">
          {renderInlineMarkdown(line.slice(2))}
        </h1>
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
          className="ml-5 list-disc space-y-2 text-neutral-700 dark:text-neutral-300"
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
      <p key={`p-${index}`} className="leading-8 text-neutral-700 dark:text-neutral-300">
        {renderInlineMarkdown(paragraphLines.join(" "))}
      </p>
    );
  }

  return <div className="space-y-6">{elements}</div>;
}
