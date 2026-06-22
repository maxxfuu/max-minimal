export interface Project {
  title: string;
  description: string;
  image: string;
  type?: "image" | "popup";
  github?: string;
  video?: string;
  link?: string;
}

export const projects: Project[] = [
  {
    title: "Yagmi",
    description:
      "Create AI Mentors that lets you chat with an “advisor” tailored to your goals, giving you guidance and next steps as you grow",
    image: "/yagmi.png",
    type: "image",
    link: "https://yagmi.app",
  },
  {
    title: "Obscuri",
    description:
      "A desktop application that silently awaits for your screenshots and querys an LLM without a trace",
    image: "/obscuri.webp",
    type: "image",
    link: "https://obscuri.app",
  },
  {
    title: "ClockIn",
    description:
      "An app that helps you stay accountable by recording timelapses of you working, so you can “clock in” with social proof",
    image: "/clockin.png",
    type: "image",
    link: "https://clockin.now",
  },
  {
    title: "Bcon",
    description:
      "A C based CLI tool that can convert data between binary value, hexadecimal, and decimal value.",
    image: "/bcon.png",
    video: "/bcon.mp4",
    type: "popup",
    github: "https://github.com/maxxfuu/bcon",
  },
];
