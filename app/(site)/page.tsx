import { Experience } from "@/components/experience";
import { Projects } from "@/components/projects";
import { Calendar } from "@/components/calendar";
import Link from "next/link";

const inlineLink =
  "border-b border-dashed border-border text-foreground transition-colors hover:border-foreground";

export default function Page() {
  return (
    <main className="mx-auto max-w-2xl px-6 pb-24 pt-12 md:px-10 md:pt-16">
      <header className="mb-20">
        <h1 className="text-4xl font-normal leading-tight tracking-tight md:text-5xl">
          Hi, I&apos;m Max
        </h1>
        <div className="my-8 space-y-6 text-base leading-[1.85] text-foreground md:text-[1.05rem]">
          <p>
            I&apos;m a full-time{" "}
            <Link href="https://www.linkedin.com/in/maxxfuu" target="_blank" className={inlineLink}>
              student
            </Link>{" "}
            studying CSE @ University of California, Merced.
          </p>
          <p>
            Growing up, I was always intrigued in working on technically challenging and visually appealing projects. Fast forward to today, I have built a collection of
            of achievements driven by passion. Over time, that fascination grew into a broader obsession with mastery and execution across different domains.
            <br /><br />
            I hope in sharing my work, you can also feel the same delight and joy in the things that I'm passionate about.
          </p>
        </div>
        <Calendar />
        <Experience />
        <Projects />
      </header>
    </main>
  );
}
