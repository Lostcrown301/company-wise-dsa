export function diffClass(diff) {
  if (!diff) return "";
  const d = diff.toLowerCase();
  if (d === "easy") return "badge-easy";
  if (d === "hard") return "badge-hard";
  return "badge-medium";
}
