export interface Resource {
  title: string;
  author?: string;
  note?: string;
  link?: string;
}

export interface ResourceGroup {
  category: string;
  description?: string;
  items: Resource[];
}

// Books, papers, and courses worth reading. Add entries here — the page at
// /resources renders every group in order.
export const resources: ResourceGroup[] = [
  {
    category: "papers",
    items: [
      {
        title: "Attention Is All You Need",
        author: "Vaswani et al., 2017",
        note: "The paper that introduced the transformer. Every language model released since is a variation on the architecture described here.",
        link: "https://arxiv.org/pdf/1706.03762",
      },
    ],
  },
];
