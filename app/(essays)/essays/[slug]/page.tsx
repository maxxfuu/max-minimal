import Link from "next/link";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { BlogMarkdown } from "@/app/(essays)/essays/components/blog-markdown";
import { formatBlogDate, getBlogPost, getBlogPosts } from "@/lib/blog";
import { createPageMetadata } from "@/lib/metadata";
import { ArrowLeftIcon } from "lucide-react";

interface BlogPostPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export async function generateMetadata({ params }: BlogPostPageProps): Promise<Metadata> {
  const { slug } = await params;
  const post = await getBlogPost(slug);

  if (!post) {
    return {};
  }

  return createPageMetadata({
    title: post.title,
    description: post.summary || post.title,
    path: `/essays/${slug}`,
    type: "article",
  });
}

export async function generateStaticParams() {
  const posts = await getBlogPosts();

  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export default async function BlogPostPage({ params }: BlogPostPageProps) {
  const { slug } = await params;
  const post = await getBlogPost(slug);

  if (!post) {
    notFound();
  }

  return (
    <main className="mx-auto max-w-2xl px-6 pb-24 pt-12 md:px-10 md:pt-16">
      <div className="mb-16 font-sans text-sm">
        <Link href="/essays" className="text-muted-foreground transition-opacity hover:text-foreground flex items-center gap-2">
          <ArrowLeftIcon className="w-4 h-4" /> back
        </Link>
      </div>

      <article>
        <header className="mb-16 text-center">
          <h1 className="text-4xl font-normal leading-[1.15] tracking-tight md:text-5xl">
            {post.title}
          </h1>
          {post.summary ? (
            <p className="mx-auto mt-6 max-w-lg text-lg leading-relaxed text-muted-foreground">
              {post.summary}
            </p>
          ) : null}
          <p className="mt-8 font-sans text-xs text-muted-foreground">
            {formatBlogDate(post.date)}
          </p>
        </header>

        <BlogMarkdown body={post.body} title={post.title} />
      </article>
    </main>
  );
}
