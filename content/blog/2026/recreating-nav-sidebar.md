---
title: "Recreating the Blog Year Nav Sidebar"
date: "2026-03-06"
summary: "A walkthrough for rebuilding the animated year-based sidebar navigation."
---

# Recreating the Blog Year Nav Sidebar

I wanted a compact navigation that could sit on the left side of the page, react to scroll position, and expand into readable year labels on hover. The result is a small sidebar that acts like a timeline for the blog archive.

The component is built around a simple list of years and matching section IDs. Each year maps to a `<section id="section-YYYY">` on the blog page, and the sidebar scrolls to that section when clicked.

## 1. Define the navigation data

Start with a typed array of years and section IDs:

```tsx
interface NavItem {
  year: number;
  sectionId: string;
}

const navItems: NavItem[] = [
  { year: 2026, sectionId: "section-2026" },
  { year: 2025, sectionId: "section-2025" },
  { year: 2024, sectionId: "section-2024" },
  { year: 2023, sectionId: "section-2023" },
  { year: 2022, sectionId: "section-2022" },
  { year: 2021, sectionId: "section-2021" },
  { year: 2020, sectionId: "section-2020" },
];
```

This gives the UI one source of truth for both the rendered controls and the sections they target.

## 2. Track the active section

The sidebar needs to know which year is currently closest to the middle of the viewport. For that, use state for:

- The active index
- Whether the sidebar is hovered
- A per-item progress value used to size and fade each bar

```tsx
const [activeIndex, setActiveIndex] = useState(2);
const [isHovered, setIsHovered] = useState(false);
const [scrollProgress, setScrollProgress] = useState<number[]>(
  navItems.map((_, i) => (i === 2 ? 1 : 0.3))
);
```

The default `2` points to `2024`, which makes that item feel selected on first render.

## 3. Update the active item on scroll

On every scroll event, inspect each target section and measure how close its midpoint is to the center of the viewport. The section with the smallest distance becomes active.

```tsx
useEffect(() => {
  const handleScroll = () => {
    const sections = navItems.map((item) =>
      document.getElementById(item.sectionId)
    );

    let newActiveIndex = 0;
    let closestDistance = Infinity;

    sections.forEach((section, index) => {
      if (section) {
        const rect = section.getBoundingClientRect();
        const sectionMiddle = rect.top + rect.height / 2;
        const distance = Math.abs(sectionMiddle - window.innerHeight / 2);

        if (distance < closestDistance) {
          closestDistance = distance;
          newActiveIndex = index;
        }
      }
    });

    setActiveIndex(newActiveIndex);

    const newProgress = navItems.map((_, index) => {
      const distanceFromActive = Math.abs(index - newActiveIndex);
      if (distanceFromActive === 0) return 1;
      if (distanceFromActive === 1) return 0.6;
      if (distanceFromActive === 2) return 0.2;
      return 0.25;
    });

    setScrollProgress(newProgress);
  };

  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll();

  return () => window.removeEventListener("scroll", handleScroll);
}, []);
```

That `newProgress` array is what gives the sidebar its “active item plus nearby neighbors” visual rhythm.

## 4. Scroll smoothly when clicking a year

Each item just needs to find its matching section and call `scrollIntoView`.

```tsx
const handleClick = (index: number) => {
  const section = document.getElementById(navItems[index].sectionId);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
};
```

This keeps the interaction simple and lets the document structure do most of the work.

## 5. Swap bars for labels on hover

The visual trick is that the default state shows thin bars, while hover hides the bars and reveals the year text in the same horizontal space.

```tsx
{navItems.map((item, index) => {
  const progress = scrollProgress[index];
  const isActive = index === activeIndex;
  const barWidth = 10 + progress * 16;
  const opacity = 0.2 + progress * 0.8;

  return (
    <button
      key={item.year}
      onClick={() => handleClick(index)}
      className="relative flex items-center justify-center h-5 cursor-pointer group"
      style={{ width: "40px" }}
      aria-label={`Navigate to ${item.year}`}
    >
      <div
        className={cn(
          "absolute left-0 bg-neutral-800 dark:bg-neutral-200 rounded-full transition-all duration-180 ease-in-out",
          isHovered && "opacity-0 blur-md scale-0"
        )}
        style={{
          width: `${barWidth}px`,
          height: "2.5px",
          opacity: isHovered ? 0 : opacity,
        }}
      />

      <span
        className={cn(
          "absolute left-0 text-sm font-medium transition-all duration-180 ease-in-out whitespace-nowrap",
          isHovered ? "opacity-100 blur-0 scale-100" : "opacity-0 blur-md scale-0",
          isActive
            ? "text-neutral-900 dark:text-neutral-100 font-semibold"
            : "text-neutral-400 dark:text-neutral-500"
        )}
        style={{ transformOrigin: "left center" }}
      >
        {item.year}
      </span>
    </button>
  );
})}
```

The result is subtle: the compact bars are great for scanning, and the hover state reveals readable labels only when needed.

## Final notes

To make this work, the page also needs matching sections like:

```tsx
<section id="section-2026">...</section>
<section id="section-2025">...</section>
<section id="section-2024">...</section>
```

Without those IDs, the sidebar would render, but clicking and active-section tracking would not line up with the page.
