import type { Metadata } from "next";
import { Geist_Mono, Figtree, Newsreader } from "next/font/google";
import "./globals.css";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { ThemeProvider } from "@/components/theme-provider";

const figtree = Figtree({ subsets: ["latin"], variable: "--font-sans" });

const newsreader = Newsreader({
  subsets: ["latin"],
  variable: "--font-serif",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Max Fu",
  description: "Software Engineer, Entrepreneur, and Student.",
  icons: {
    icon: "/favicon.ico",
  },
  openGraph: {
    title: "Max Fu",
    description: "Software Engineer, Entrepreneur, and Student.",
    siteName: "Max Fu",
    images: [
      {
        url: "/favicon.ico",
        width: 1200,
        height: 630,
        alt: "Max Fu",
      },
    ],
    locale: "en_US",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${figtree.variable} ${newsreader.variable}`} suppressHydrationWarning>
      <body className={`${geistMono.variable} min-h-screen bg-background font-serif text-foreground antialiased [font-family:var(--font-serif),ui-serif,Georgia,serif]`}>
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
          <SiteHeader />
          {children}
          <SiteFooter />
        </ThemeProvider>
      </body>
    </html>
  );
}
