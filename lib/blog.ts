import fs from "node:fs/promises";
import path from "node:path";

export const BLOG_YEARS = [2026, 2025, 2024, 2023, 2022, 2021, 2020];

const blogContentDirectory = path.join(process.cwd(), "content", "blog");

export interface BlogPost {
  slug: string;
  year: number;
  title: string;
  date: string;
  summary: string;
  body: string;
  href: string;
}

function parseFrontmatter(fileContent: string) {
  const frontmatterMatch = fileContent.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);

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
        const value = line.slice(separatorIndex + 1).trim().replace(/^"|"$/g, "");

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

  const markdownFiles = entries.filter((entry) => entry.isFile() && entry.name.endsWith(".md"));

  const posts = await Promise.all(
    markdownFiles.map(async (entry) => {
      const relativePath = entry.parentPath
        ? path.relative(blogContentDirectory, path.join(entry.parentPath, entry.name))
        : entry.name;
      const fullPath = path.join(blogContentDirectory, relativePath);
      const fileContent = await fs.readFile(fullPath, "utf8");
      const { metadata, body } = parseFrontmatter(fileContent);
      const [yearDirectory, ...rest] = relativePath.replace(/\.md$/, "").split(path.sep);
      const year = Number(yearDirectory);
      const slug = rest.join("/");

      if (!Number.isFinite(year) || !slug) {
        return null;
      }

      return {
        slug,
        year,
        title: String(metadata.title ?? slug),
        date: String(metadata.date ?? `${year}-01-01`),
        summary: String(metadata.summary ?? ""),
        body,
        href: `/blog/${year}/${slug}`,
      };
    })
  );

  return posts
    .filter((post): post is BlogPost => post !== null)
    .sort((a, b) => b.date.localeCompare(a.date));
}

export async function getBlogPost(year: number, slug: string) {
  const posts = await getBlogPosts();

  return posts.find((post) => post.year === year && post.slug === slug) ?? null;
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
  }).format(parsedDate);
}
