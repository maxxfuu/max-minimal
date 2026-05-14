import Link from "next/link";
import { notFound } from "next/navigation";
import { BlogMarkdown } from "@/app/blog/components/blog-markdown";
import { formatBlogDate, getBlogPost, getBlogPosts } from "@/lib/blog";

interface BlogPostPageProps {
  params: Promise<{
    year: string;
    slug: string;
  }>;
}

export async function generateStaticParams() {
  const posts = await getBlogPosts();

  return posts.map((post) => ({
    year: String(post.year),
    slug: post.slug,
  }));
}

export default async function BlogPostPage({ params }: BlogPostPageProps) {
  const { year, slug } = await params;
  const numericYear = Number(year);
  const post = await getBlogPost(numericYear, slug);

  if (!post) {
    notFound();
  }

  return (
    <main className="min-h-screen px-6 py-8 md:px-10">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8">
          <Link
            href="/blog"
            className="inline-flex items-center rounded-full border border-neutral-200 px-4 py-2 text-sm text-neutral-700 transition-colors hover:border-neutral-300 hover:text-neutral-950 dark:border-neutral-800 dark:text-neutral-300 dark:hover:border-neutral-700 dark:hover:text-neutral-100"
          >
            &lt; Back to blog
          </Link>
        </div>

        <article className="rounded-[2rem] border border-neutral-200/80 bg-white/80 p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-950/70 md:p-12">
          <header className="mb-10">
            <p className="text-sm text-neutral-500 dark:text-neutral-400">
              {formatBlogDate(post.date)}
            </p>
            <h1 className="mt-3 text-4xl font-semibold tracking-tight md:text-5xl">
              {post.title}
            </h1>
            {post.summary ? (
              <p className="mt-4 max-w-2xl text-lg text-neutral-600 dark:text-neutral-300">
                {post.summary}
              </p>
            ) : null}
          </header>

          <BlogMarkdown body={post.body} />
        </article>
      </div>
    </main>
  );
}
