import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeftIcon } from "lucide-react";
import { Projects } from "@/components/projects";
import { createPageMetadata } from "@/lib/metadata";

export const metadata: Metadata = createPageMetadata({
  title: "Projects",
  description: "A collection of things I've built — apps, tools, and experiments.",
  path: "/projects",
});

export default function ProjectsPage() {
  return (
    <main className="mx-auto max-w-2xl px-6 pb-24 pt-12 md:px-10 md:pt-16">
      <div className="mb-16 font-sans text-sm">
        <Link
          href="/"
          className="flex items-center gap-2 text-muted-foreground transition-opacity hover:text-foreground"
        >
          <ArrowLeftIcon className="h-4 w-4" /> back
        </Link>
      </div>

      <header className="mb-12">
        <h1 className="text-4xl font-normal leading-tight tracking-tight md:text-5xl">
          Projects
        </h1>
        <p className="mt-2 max-w-lg text-base leading-relaxed text-muted-foreground">
          Apps, tools, and experiments I&apos;ve shipped along the way.
        </p>
      </header>

      <Projects />
    </main>
  );
}
