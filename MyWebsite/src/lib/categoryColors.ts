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
