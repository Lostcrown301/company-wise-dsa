import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { diffClass } from "../components/utils.js";
import { getRandomQuestions } from "../api.js";
import { useProgress } from "../context/ProgressContext.jsx";

export default function PracticeSessionPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  
  const { isSolved, toggleSolved } = useProgress();

  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const params = {};
        if (queryParams.has("company")) params.company = queryParams.get("company");
        if (queryParams.has("topic")) params.topic = queryParams.get("topic");
        if (queryParams.has("difficulty")) params.difficulty = queryParams.get("difficulty");
        params.limit = queryParams.get("limit") || "10";
        
        const data = await getRandomQuestions(params);
        setQuestions(data);
      } catch (err) {
        console.error("Failed to fetch practice session", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchSession();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.search]);

  if (isLoading) {
    return (
      <main style={{ maxWidth: 560, margin: "0 auto", padding: "0 24px", paddingTop: 56 }}>
        <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>Loading session...</div>
      </main>
    );
  }

  if (questions.length === 0) {
    return (
      <main style={{ maxWidth: 560, margin: "0 auto", padding: "0 24px", paddingTop: 56 }}>
        <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "24px", color: "var(--foreground)", margin: "0 0 16px" }}>No Questions Found</h1>
        <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)", marginBottom: 24 }}>Try adjusting your filters.</p>
        <button onClick={() => navigate("/practice")} style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--accent)", background: "none", border: "none", cursor: "pointer", padding: 0 }}>
          ← Back to setup
        </button>
      </main>
    );
  }

  const q = questions[current];
  const total = questions.length;
  
  // Calculate how many of the session questions are solved currently
  const sessionSolvedCount = questions.filter(q => isSolved(q.slug)).length;
  
  // PCT is based on current index out of total (just progress through the session, or based on solved count? We'll base it on current position as in original code)
  const isCurrentSolved = isSolved(q.slug);
  const pct = ((current + (isCurrentSolved ? 1 : 0)) / total) * 100;

  return (
    <main style={{ maxWidth: 560, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 64 }}>
        <div style={{ marginBottom: 40 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
            <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12, color: "var(--muted-foreground)" }}>Question {String(current + 1).padStart(2, "0")} / {String(total).padStart(2, "0")}</span>
            <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12, color: "var(--muted-foreground)" }}>{sessionSolvedCount} solved</span>
          </div>
          <div className="progress-bar">
            <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
          </div>
        </div>

        <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(24px, 4vw, 36px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: "0 0 8px" }}>{q.title}</h1>
        <span className={diffClass(q.difficulty)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12, display: "block", marginBottom: 32 }}>
          {q.difficulty.charAt(0).toUpperCase() + q.difficulty.slice(1)}
        </span>

        <a href={q.leetcode_url} target="_blank" rel="noopener noreferrer" style={{ display: "inline-flex", alignItems: "center", gap: 6, fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 14, color: "var(--accent)", textDecoration: "none", borderBottom: "1px solid var(--accent)", paddingBottom: 1, marginBottom: 36 }}>
          Open on LeetCode ↗
        </a>

        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <button
            onClick={() => toggleSolved(q.slug)}
            style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 14, color: isCurrentSolved ? "var(--primary-foreground)" : "var(--foreground)", backgroundColor: isCurrentSolved ? "var(--accent)" : "transparent", border: "1px solid var(--border)", borderRadius: "var(--radius)", padding: "10px 20px", cursor: "pointer", transition: "background-color 150ms ease, color 150ms ease" }}
          >
            {isCurrentSolved ? "✓ Solved" : "Mark solved"}
          </button>
          <button
            onClick={() => { if (current < total - 1) setCurrent((v) => v + 1); else navigate("/progress"); }}
            style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 14, color: "var(--foreground)", backgroundColor: "transparent", border: "1px solid var(--border)", borderRadius: "var(--radius)", padding: "10px 20px", cursor: "pointer" }}
          >
            {current < total - 1 ? "Next →" : "Finish session →"}
          </button>
        </div>

        <button onClick={() => navigate("/")} style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)", background: "none", border: "none", cursor: "pointer", padding: "24px 0 0", display: "block" }}>
          End session
        </button>
      </section>
    </main>
  );
}
