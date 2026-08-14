import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { getQuestions } from "../api.js";
import { diffClass } from "../components/utils.js";
import { useProgress } from "../context/ProgressContext.jsx";

export default function QuestionDetailPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const slug = queryParams.get("slug");

  const { isSolved, isBookmarked, getNote, toggleSolved, toggleBookmarked, saveNote } = useProgress();
  
  const [question, setQuestion] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Local state for the note textarea to prevent lagging on every keystroke, synced on blur/timeout
  const [localNote, setLocalNote] = useState("");

  useEffect(() => {
    if (!slug) {
      navigate("/questions");
      return;
    }

    const fetchQuestion = async () => {
      try {
        const data = await getQuestions({ slugs: slug, limit: 1 });
        if (data.items && data.items.length > 0) {
          setQuestion(data.items[0]);
        } else {
          navigate("/questions"); // not found
        }
      } catch (err) {
        console.error("Failed to fetch question detail", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchQuestion();
  }, [slug, navigate]);

  useEffect(() => {
    if (slug) {
      setLocalNote(getNote(slug));
    }
  }, [slug, getNote]);

  const handleNoteChange = (e) => {
    setLocalNote(e.target.value);
  };

  const handleNoteBlur = () => {
    if (slug) {
      saveNote(slug, localNote);
    }
  };

  if (isLoading) {
    return (
      <main style={{ maxWidth: 680, margin: "0 auto", padding: "0 24px", paddingTop: 40 }}>
        <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>Loading question...</div>
      </main>
    );
  }

  if (!question) return null;

  const solved = isSolved(slug);
  const bookmarked = isBookmarked(slug);

  // Combine company and topic tags
  const tags = [
    ...question.topics.map(t => t.name),
    ...question.companies.map(c => c.name)
  ];

  return (
    <main style={{ maxWidth: 680, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 40, paddingBottom: 64 }}>
        <button onClick={() => navigate(-1)} style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)", background: "none", border: "none", cursor: "pointer", padding: 0, marginBottom: 24, display: "block" }}>
          ← Back
        </button>


        <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(24px, 4vw, 40px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: "0 0 12px" }}>
          {question.title}
        </h1>

        <div style={{ display: "flex", alignItems: "center", gap: 14, flexWrap: "wrap", marginBottom: 32 }}>
          <span className={diffClass(question.difficulty)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12 }}>
            {question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1)}
          </span>
          {tags.map((tag) => (
            <span key={tag} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12, color: "var(--muted-foreground)", border: "1px solid var(--border)", borderRadius: "var(--radius)", padding: "2px 8px" }}>{tag}</span>
          ))}
        </div>

        <a href={question.leetcode_url} target="_blank" rel="noopener noreferrer" style={{ display: "inline-flex", alignItems: "center", gap: 6, fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 14, color: "var(--accent)", textDecoration: "none", borderBottom: "1px solid var(--accent)", paddingBottom: 1, marginBottom: 36 }}>
          Open on LeetCode ↗
        </a>

        <hr className="divider" style={{ marginBottom: 28 }} />

        <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 40 }}>
          <button
            onClick={() => toggleSolved(slug)}
            style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 14, color: solved ? "var(--primary-foreground)" : "var(--foreground)", backgroundColor: solved ? "var(--accent)" : "transparent", border: "1px solid var(--border)", borderRadius: "var(--radius)", padding: "9px 18px", cursor: "pointer", transition: "background-color 150ms ease, color 150ms ease" }}
          >
            {solved ? "✓ Solved" : "Mark solved"}
          </button>
          <button
            onClick={() => toggleBookmarked(slug)}
            style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: bookmarked ? "var(--accent)" : "var(--muted-foreground)", backgroundColor: "transparent", border: "1px solid var(--border)", borderRadius: "var(--radius)", padding: "9px 18px", cursor: "pointer", transition: "color 150ms ease" }}
          >
            {bookmarked ? "◆ Bookmarked" : "◇ Bookmark"}
          </button>
        </div>

        <div>
          <label style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--muted-foreground)", display: "block", marginBottom: 10 }}>
            Personal notes
          </label>
          <textarea
            value={localNote}
            onChange={handleNoteChange}
            onBlur={handleNoteBlur}
            placeholder="Add notes, approach, time complexity…"
            style={{ width: "100%", minHeight: 160, border: "1px solid var(--border)", borderRadius: "var(--radius)", backgroundColor: "var(--card)", color: "var(--foreground)", fontFamily: "var(--font-dm-sans)", fontSize: 14, lineHeight: 1.6, padding: "12px 14px", resize: "vertical", outline: "none", transition: "border-color 120ms ease" }}
            onFocus={(e) => (e.target.style.borderColor = "var(--accent)")}
          />
        </div>
      </section>
    </main>
  );
}
