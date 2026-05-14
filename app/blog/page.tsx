import Link from "next/link";
import { BLOG_YEARS, formatBlogDate, getBlogPosts } from "@/lib/blog";
import { NavSidebar } from "./components/nav-sidebar";

export default async function Blog() {
  const posts = await getBlogPosts();
  const postsByYear = new Map<number, Awaited<ReturnType<typeof getBlogPosts>>>();

  BLOG_YEARS.forEach((year) => {
    postsByYear.set(
      year,
      posts.filter((post) => post.year === year)
    );
  });

  return (
    <>
      <NavSidebar />
      <div className="min-h-screen flex flex-col justify-center items-center px-8 text-center">
        <h1 className="text-sm font-semibold">
          A collection of my literary atrocities on anything tech and life
        </h1>
      </div>

      {BLOG_YEARS.map((year) => {
        const yearPosts = postsByYear.get(year) ?? [];

        return (
          <section
            key={year}
            id={`section-${year}`}
            className="min-h-screen px-8 py-8 md:px-20"
          >
            <div className="mx-auto flex max-w-4xl flex-col">
              <div>
                <h2 className="text-5xl font-bold text-neutral-200 dark:text-neutral-800 md:text-6xl">
                  {year}
                </h2>
                <p className="mt-3 max-w-md text-neutral-400 dark:text-neutral-500">
                  {yearPosts.length > 0
                    ? `${yearPosts.length} post${yearPosts.length === 1 ? "" : "s"} from ${year}.`
                    : `Nothing from ${year} yet, check back later!`}
                </p>
              </div>

              {yearPosts.length > 0 ? (
                <div className="space-y-8">
                  {yearPosts.map((post) => (
                    <Link
                      key={post.slug}
                      href={post.href}
                      className="grid gap-6 bg-white/70 p-8 transition-colors hover:border-neutral-300 dark:border-neutral-800 dark:bg-neutral-950/60 dark:hover:border-neutral-700 md:grid-cols-[minmax(0,1fr)_auto] md:items-start"
                    >
                      <div>
                        <h3 className="text-2xl font-semibold">{post.title}</h3>
                        {post.summary ? (
                          <p className="mt-3 max-w-2xl text-neutral-600 dark:text-neutral-300">
                            {post.summary}
                          </p>
                        ) : null}
                      </div>

                      <p className="text-sm text-neutral-500 dark:text-neutral-400 md:pt-1">
                        {formatBlogDate(post.date)}
                      </p>
                    </Link>
                  ))}
                </div>
              ) : null}
            </div>
          </section>
        );
      })}
    </>
  );
}