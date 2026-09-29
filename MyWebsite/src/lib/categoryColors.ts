// Central color palette for professional categories and engagement roles.
// Shared between ExperienceItem.astro (chip colors) and index.astro (color-coded legend).

export interface ColorPair { bg: string; fg: string; }

export const CAT_COLORS: Record<string, ColorPair> = {
  "Auditing & Compliance": { bg: "#E8EEF7", fg: "#1D4289" },      // blue
  "Business Intelligence": { bg: "#E0F5F1", fg: "#0E6B63" },       // teal
  "Finance Automation": { bg: "#ECE9F7", fg: "#4B3FA0" },          // indigo
  "Finance Transformation": { bg: "#F2ECFA", fg: "#7A308F" },      // purple
  "Financial Modelling & Cash Flow": { bg: "#EEF3F2", fg: "#3E5755" },  // slate
  "Financial Planning & Control": { bg: "#E0F4F6", fg: "#0E6A82" },   // cyan
  "Financial Reporting / IFRS": { bg: "#FDF3DD", fg: "#B45309" },   // amber
  "Group Controlling & M&A": { bg: "#FDE8EC", fg: "#B3142B" },     // red
  "Interim CFO / Fundraising": { bg: "#F9E6EF", fg: "#9C1560" },   // pink
  "Non-profit & Community": { bg: "#E7F6EC", fg: "#167A3C" },      // green
  "Real Estate / Corporate Development": { bg: "#FDE6D4", fg: "#B8410C" }, // orange
  "SAP / ERP Transformation": { bg: "#E0F5FA", fg: "#0E6A85" },    // cyan-blue
  "Valuation / Operations": { bg: "#E8EEF8", fg: "#2741B0" },      // deep blue
  "Business Analysis": { bg: "#F3EEFF", fg: "#5B59C9" },           // indigo
  "Project Management": { bg: "#EAF4FF", fg: "#1673B3" },          // blue
  "Strategy": { bg: "#EAFBE9", fg: "#2B8A3E" },                    // green
  "Business Development": { bg: "#FFF3D0", fg: "#B76000" },        // amber
  "Marketing": { bg: "#FDE8EC", fg: "#C0244F" },                   // red
  "Data Management": { bg: "#E6F3FF", fg: "#0A6CC0" },            // cyan
  "Gap Analysis": { bg: "#F1F5EE", fg: "#4A7C32" },              // dark green
  "Artificial Intelligence": { bg: "#EDE7F6", fg: "#6B4FB0" },     // violet
  "Negotiation": { bg: "#FDECE0", fg: "#C24E0B" },                // orange
  "ERP transformation": { bg: "#E0F5FA", fg: "#0A6E85" },        // cyan
  "Finance closing": { bg: "#FDF3DD", fg: "#B45309" },          // amber
  "IFRS": { bg: "#FDF3DD", fg: "#B45309" },                    // amber
  "Regulatory reporting": { bg: "#FCE9E9", fg: "#A1262A" },      // red-amber
  "Budgeting": { bg: "#E0F4F6", fg: "#0E6A82" },            // cyan
  "Accounting": { bg: "#E7F6EC", fg: "#167A3C" },            // green
  "Finance transformation": { bg: "#F2ECFA", fg: "#7A308F" },   // purple
  "Fundraising": { bg: "#F9E6EF", fg: "#9C1560" },           // pink
  "Financial modelling": { bg: "#EEF3F2", fg: "#3E5755" },      // slate
  "Cash-flow management": { bg: "#EEF3F2", fg: "#3E5755" },     // slate
  "Business analyst": { bg: "#F3EEFF", fg: "#5B59C9" },        // indigo
  "Automation": { bg: "#ECE9F7", fg: "#4B3FA0" },            // indigo
  "Project management": { bg: "#EAF4FF", fg: "#1673B3" },       // blue
  "Data management": { bg: "#E6F3FF", fg: "#0A6CC0" },         // cyan
  "Strategy": { bg: "#EAFBE9", fg: "#2B8A3E" },               // green
  "Business development": { bg: "#FFF3D0", fg: "#B76000" },      // amber
  "Marketing": { bg: "#FDE8EC", fg: "#C0244F" },              // red
  "Advisory": { bg: "#EDE7F6", fg: "#6B4FB0" },             // violet
  "Cursus Grand Talent": { bg: "#EDE7F6", fg: "#5B21B6" },     // indigo
};

export const ROLE_COLORS: Record<string, ColorPair> = {
  "Freelancer": { bg: "#0b6fe0", fg: "#ffffff" },
  "Internal": { bg: "#475569", fg: "#ffffff" },
};

export const FALLBACK_COLOR: ColorPair = { bg: "#f0f4fb", fg: "#0958b8" };

// Resolve a named item's color, falling back to a neutral when unknown.
export function resolveColor(name: string, palette?: Record<string, ColorPair>): ColorPair {
  return (palette && palette[name]) || FALLBACK_COLOR;
}

export function styleString(name: string, palette?: Record<string, ColorPair>): string {
  const c = resolveColor(name, palette);
  return `background:${c.bg};color:${c.fg}`;
}
