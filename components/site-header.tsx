"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ThemeToggle } from "@/components/theme-toggle";

function navLabel(active: boolean, label: string) {
  return active ? `• ${label}` : label;
}

export function SiteHeader() {
  const pathname = usePathname();
  const isHome = pathname === "/";
  const isEssays = pathname.startsWith("/blog");
  const isResume = pathname === "/resume";

  return (
    <header className="mx-auto flex max-w-5xl items-start justify-between px-6 pt-10 md:px-10 md:pt-14">
      <Link
        href="/"
        className="font-sans text-sm tracking-wide text-foreground lowercase transition-opacity hover:opacity-60"
      >
        maxxfuu
      </Link>

      <nav className="flex flex-col items-end gap-1 font-sans text-sm lowercase text-muted-foreground">
        <Link
          href="/"
          className={isHome ? "text-foreground" : "transition-colors hover:text-foreground"}
        >
          {navLabel(isHome, "home")}
        </Link>
        <Link
          href="/blog"
          className={isEssays ? "text-foreground" : "transition-colors hover:text-foreground"}
        >
          {navLabel(isEssays, "essays")}
        </Link>
        <Link
          href="/resume"
          className={isResume ? "text-foreground" : "transition-colors hover:text-foreground"}
        >
          {navLabel(isResume, "resume")}
        </Link>
        <ThemeToggle />
      </nav>
    </header>
  );
}
