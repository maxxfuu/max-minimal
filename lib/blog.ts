import fs from "node:fs/promises";
import path from "node:path";

const blogContentDirectory = path.join(process.cwd(), "content", "blog");

export interface BlogPost {
  slug: string;
  title: string;
  date: string;
  summary: string;
  body: string;
  href: string;
}

function normalizeDashes(value: string) {
  return value.replace(/[\u2010-\u2015\u2212\uFE58\uFE63\uFF0D]/g, "-");
}

function parseFrontmatter(fileContent: string) {
  const normalizedContent = normalizeDashes(fileContent);
  const frontmatterMatch = normalizedContent.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);

  if (!frontmatterMatch) {
    return {
      metadata: {},
      body: fileContent.trim(),
    };
  }

  const [, frontmatter, body] = frontmatterMatch;
  const metadata = Object.fromEntries(
    frontmatter
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => {
        const separatorIndex = line.indexOf(":");

        if (separatorIndex === -1) {
          return [line, ""];
        }

        const key = line.slice(0, separatorIndex).trim();
        const value = normalizeDashes(
          line.slice(separatorIndex + 1).trim().replace(/^"|"$/g, "")
        );

        return [key, value];
      })
  );

  return {
    metadata,
    body: body.trim(),
  };
}

export async function getBlogPosts(): Promise<BlogPost[]> {
  const entries = await fs.readdir(blogContentDirectory, {
    recursive: true,
    withFileTypes: true,
  });

  const markdownFiles = entries.filter(
    (entry) => entry.isFile() && entry.name.endsWith(".md") && entry.name !== "README.md"
  );

  const posts = await Promise.all(
    markdownFiles.map(async (entry) => {
      const relativePath = entry.parentPath
        ? path.relative(blogContentDirectory, path.join(entry.parentPath, entry.name))
        : entry.name;
      const fullPath = path.join(blogContentDirectory, relativePath);
      const fileContent = await fs.readFile(fullPath, "utf8");
      const { metadata, body } = parseFrontmatter(fileContent);
      const slug = path.basename(relativePath, ".md");

      if (!slug) {
        return null;
      }

      return {
        slug,
        title: String(metadata.title ?? slug),
        date: String(metadata.date ?? "1970-01-01"),
        summary: String(metadata.summary ?? ""),
        body,
        href: `/blog/${slug}`,
      };
    })
  );

  return posts
    .filter((post): post is BlogPost => post !== null)
    .sort((a, b) => b.date.localeCompare(a.date));
}

export async function getBlogPost(slug: string) {
  const posts = await getBlogPosts();

  return posts.find((post) => post.slug === slug) ?? null;
}

export function formatBlogDate(date: string) {
  const parsedDate = new Date(date);

  if (Number.isNaN(parsedDate.getTime())) {
    return date;
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  })
    .format(parsedDate);
}
