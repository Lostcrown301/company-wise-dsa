import { useNavigate } from "react-router-dom";
import { diffClass } from "./utils.js";
import { useProgress } from "../context/ProgressContext.jsx";

export default function QuestionTable({ questions, startIndex = 1 }) {
  const navigate = useNavigate();
  const { isSolved, isBookmarked } = useProgress();

  return (
    <>
      <div className="q-desktop" style={{ display: "grid", gridTemplateColumns: "52px 1fr 88px 72px 56px 48px", gap: 12, padding: "8px 0", borderBottom: "1px solid var(--border)" }}>
        {["#", "Question", "Difficulty", "Freq", "✓", "◆"].map((h, i) => (
          <span key={i} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", color: "var(--muted-foreground)", textTransform: "uppercase", textAlign: i >= 4 ? "center" : "left" }}>{h}</span>
        ))}
      </div>

      {questions.map((q, i) => {
        const solved = isSolved(q.slug);
        const bookmarked = isBookmarked(q.slug);
        const numStr = String(startIndex + i);
        const diffStr = q.difficulty ? q.difficulty.charAt(0).toUpperCase() + q.difficulty.slice(1) : "";
        const freqStr = q.frequency !== undefined && q.frequency !== null ? q.frequency.toFixed(1) : "--";

        return (
          <div
            key={q.slug}
            className="row-hover"
            style={{ borderBottom: i < questions.length - 1 ? "1px solid var(--border)" : "none", cursor: "pointer" }}
            onClick={() => navigate(`/questions/detail?slug=${q.slug}`)}
          >
            <div className="q-desktop" style={{ display: "grid", gridTemplateColumns: "52px 1fr 88px 72px 56px 48px", gap: 12, padding: "12px 0", alignItems: "center" }}>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12, color: "var(--muted-foreground)" }}>{numStr}</span>
              <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--foreground)" }}>{q.title}</span>
              <span className={diffClass(q.difficulty)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12 }}>{diffStr}</span>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12, color: "var(--muted-foreground)" }}>{freqStr}</span>
              <span style={{ textAlign: "center", fontSize: 13, color: solved ? "var(--accent)" : "var(--border)" }}>{solved ? "✓" : "○"}</span>
              <span style={{ textAlign: "center", fontSize: 13, color: bookmarked ? "var(--accent)" : "var(--border)" }}>{bookmarked ? "◆" : "◇"}</span>
            </div>

            <div className="q-mobile" style={{ padding: "12px 0", display: "none" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 8 }}>
                <div>
                  <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, color: "var(--muted-foreground)", marginRight: 8 }}>{numStr}</span>
                  <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--foreground)" }}>{q.title}</span>
                </div>
                <div style={{ display: "flex", gap: 8, flexShrink: 0 }}>
                  <span style={{ fontSize: 12, color: solved ? "var(--accent)" : "var(--border)" }}>{solved ? "✓" : "○"}</span>
                  <span style={{ fontSize: 12, color: bookmarked ? "var(--accent)" : "var(--border)" }}>{bookmarked ? "◆" : "◇"}</span>
                </div>
              </div>
              <div style={{ marginTop: 4, display: "flex", gap: 16 }}>
                <span className={diffClass(q.difficulty)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11 }}>{diffStr}</span>
                <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, color: "var(--muted-foreground)" }}>freq {freqStr}</span>
              </div>
            </div>
          </div>
        );
      })}

      <style>{`
        @media (max-width: 640px) {
          .q-desktop { display: none !important; }
          .q-mobile { display: block !important; }
        }
      `}</style>
    </>
  );
}
