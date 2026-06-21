import { Experience } from "@/components/experience";
import { Projects } from "@/components/projects";
import { Calendar } from "@/components/calendar";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
import { Separator } from "@/components/ui/separator"
import Link from "next/link";
import { ArrowRightIcon } from "lucide-react";

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
            Growing up, I was always intrigued in working on technically challenging and visually appealing projects. Fast forward to today, I have built a
             <HoverCard>
              <HoverCardTrigger> <span className="border-b border-dashed border-muted-foreground text-foreground transition-colors hover:border-foreground cursor-pointer">collection</span></HoverCardTrigger>
              <HoverCardContent>
                <p className="font-semibold">Achievements and interests:</p>
                <ul>
                  <li>- Programming</li>
                  <li>- Cooking</li>
                  <li>- Powerlifting</li>
                  <li>- Design</li>
                  <li>- Reading</li>
                  <li>- Marketing</li>
                  <li>- Writing</li>
                  <li>- Filming</li>
                  <li>- Golfing</li>
                </ul>
              </HoverCardContent>
            </HoverCard>
            {} of interests and achievements driven by passion. Over time, that fascination grew into a broader obsession with mastery and execution across different domains.
            <br /><br />
            I hope in sharing my work and experiences, you can also feel the same delight and joy in the things that I'm passionate about.
          </p>
        </div>
        <Link href="/blog" className="text-sm text-foreground transition-opacity hover:text-foreground flex items-center justify-end gap-2 mb-8">
          Essays 
          <ArrowRightIcon className="w-4 h-4" />
        </Link>
        <Separator />
        <div className="mt-16">
          <Calendar />
          <Experience />
          <Projects />
        </div>
      </header>
    </main>
  );
}
