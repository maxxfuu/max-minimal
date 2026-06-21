import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="mx-auto max-w-2xl px-6 pb-16 pt-24 text-center font-sans text-xs lowercase text-muted-foreground md:px-10">
      <p>
        <Link href="https://www.linkedin.com/in/maxxfuu" target="_blank" className="transition-colors hover:text-foreground">
          linkedin
        </Link>
        {" · "}
        <Link href="https://github.com/maxxfuu" target="_blank" className="transition-colors hover:text-foreground">
          github
        </Link>
        {" · "}
        <Link href="https://leetcode.com/maxxfuu" target="_blank" className="transition-colors hover:text-foreground">
          leetcode
        </Link>
      </p>
      <p className="mt-3">maxxfuu · {new Date().getFullYear()}</p>
    </footer>
  );
}
