import { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useProgress } from "../context/ProgressContext.jsx";
import { getQuestions } from "../api.js";
import { diffClass } from "../components/utils.js";

export default function ProgressPage() {
  const navigate = useNavigate();
  const { progress } = useProgress();
  
  const [totals, setTotals] = useState({ easy: 0, medium: 0, hard: 0, all: 0 });
  const [metadataMap, setMetadataMap] = useState(new Map());
  const [isLoading, setIsLoading] = useState(true);

  // Notes with actual content
  const notesCount = useMemo(() => {
    return Object.values(progress.notes).filter(n => n && n.trim().length > 0).length;
  }, [progress.notes]);

  const solvedSlugs = Object.keys(progress.solved);
  const bookmarkedSlugs = progress.bookmarked;

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [allReq, easyReq, medReq, hardReq] = await Promise.all([
          getQuestions({ limit: 1 }),
          getQuestions({ difficulty: "easy", limit: 1 }),
          getQuestions({ difficulty: "medium", limit: 1 }),
          getQuestions({ difficulty: "hard", limit: 1 })
        ]);
        setTotals({
          all: allReq.total,
          easy: easyReq.total,
          medium: medReq.total,
          hard: hardReq.total
        });
      } catch (err) {
        console.error("Failed to fetch denominators", err);
      }
    };
    fetchStats();
  }, []);

  useEffect(() => {
    const fetchMetadata = async () => {
      const allSlugs = Array.from(new Set([...solvedSlugs, ...bookmarkedSlugs]));
      if (allSlugs.length === 0) {
        setMetadataMap(new Map());
        setIsLoading(false);
        return;
      }

      try {
        const batchSize = 100;
        const newMap = new Map();
        for (let i = 0; i < allSlugs.length; i += batchSize) {
          const batch = allSlugs.slice(i, i + batchSize).join(",");
          const data = await getQuestions({ slugs: batch, limit: 100 });
          data.items.forEach(q => newMap.set(q.slug, q));
        }
        setMetadataMap(newMap);
      } catch (err) {
        console.error("Failed to fetch metadata", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMetadata();
  }, [solvedSlugs.length, bookmarkedSlugs.length]); // Re-fetch if lengths change

  // Calculate difficulty numerators
  const diffSolved = useMemo(() => {
    let easy = 0, medium = 0, hard = 0;
    for (const slug of solvedSlugs) {
      const m = metadataMap.get(slug);
      if (m) {
        if (m.difficulty === "easy") easy++;
        else if (m.difficulty === "medium") medium++;
        else if (m.difficulty === "hard") hard++;
      }
    }
    return { easy, medium, hard };
  }, [solvedSlugs, metadataMap]);

  // Recently solved
  const recentSolved = useMemo(() => {
    return Object.entries(progress.solved)
      .map(([slug, data]) => ({ slug, ...data }))
      .sort((a, b) => new Date(b.solvedAt) - new Date(a.solvedAt))
      .slice(0, 5)
      .map(entry => metadataMap.get(entry.slug))
      .filter(Boolean);
  }, [progress.solved, metadataMap]);

  // Bookmarks
  const bookmarksList = useMemo(() => {
    return bookmarkedSlugs
      .map(slug => metadataMap.get(slug))
      .filter(Boolean);
  }, [bookmarkedSlugs, metadataMap]);

  return (
    <main style={{ maxWidth: 680, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 64 }}>
        <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(28px, 5vw, 44px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: "0 0 32px" }}>My Progress</h1>

        <div style={{ display: "flex", gap: "clamp(24px, 5vw, 56px)", flexWrap: "wrap", marginBottom: 48 }}>
          {[{ val: solvedSlugs.length.toString(), label: "solved" }, { val: bookmarkedSlugs.length.toString(), label: "bookmarked" }, { val: notesCount.toString(), label: "notes" }].map(({ val, label }) => (
            <div key={label}>
              <div style={{ fontFamily: "var(--font-dm-mono)", fontSize: "clamp(28px, 4vw, 40px)", fontWeight: 300, color: "var(--foreground)", letterSpacing: "-0.03em" }}>{val}</div>
              <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)", marginTop: 2 }}>{label}</div>
            </div>
          ))}
        </div>

        <hr className="divider" style={{ marginBottom: 36 }} />

        <div style={{ marginBottom: 48 }}>
          <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", color: "var(--muted-foreground)", textTransform: "uppercase", display: "block", marginBottom: 20 }}>By difficulty</span>
          {[
            { label: "Easy", solved: diffSolved.easy, total: totals.easy },
            { label: "Medium", solved: diffSolved.medium, total: totals.medium },
            { label: "Hard", solved: diffSolved.hard, total: totals.hard },
          ].map(({ label, solved, total }) => (
            <div key={label} style={{ marginBottom: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                <span className={diffClass(label)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12 }}>{label}</span>
                <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12, color: "var(--muted-foreground)" }}>{solved} / {total > 0 ? total.toLocaleString() : "--"}</span>
              </div>
              <div className="progress-bar">
                <div className="progress-bar-fill" style={{ width: total > 0 ? `${(solved / total) * 100}%` : "0%" }} />
              </div>
            </div>
          ))}
        </div>

        <hr className="divider" style={{ marginBottom: 36 }} />

        <div style={{ marginBottom: 48 }}>
          <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", color: "var(--muted-foreground)", textTransform: "uppercase", display: "block", marginBottom: 16 }}>Recently solved</span>
          {isLoading ? (
            <div style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>Loading...</div>
          ) : recentSolved.length > 0 ? (
            recentSolved.map((q, i) => (
              <div
                key={q.slug}
                className="row-hover"
                onClick={() => navigate(`/questions/detail?slug=${q.slug}`)}
                style={{ display: "flex", alignItems: "center", gap: 14, padding: "10px 0", borderBottom: i < recentSolved.length - 1 ? "1px solid var(--border)" : "none", cursor: "pointer" }}
              >
                <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, color: "var(--muted-foreground)", minWidth: 24 }}>{String(i + 1)}</span>
                <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--foreground)", flex: 1 }}>{q.title}</span>
                <span className={diffClass(q.difficulty)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11 }}>{q.difficulty.charAt(0).toUpperCase() + q.difficulty.slice(1)}</span>
              </div>
            ))
          ) : (
             <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>No recently solved questions.</div>
          )}
        </div>

        {bookmarksList.length > 0 && (
          <>
            <hr className="divider" style={{ marginBottom: 36 }} />
            <div style={{ marginBottom: 48 }}>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", color: "var(--muted-foreground)", textTransform: "uppercase", display: "block", marginBottom: 16 }}>Bookmarks</span>
              {bookmarksList.map((q, i) => (
                <div
                  key={q.slug}
                  className="row-hover"
                  onClick={() => navigate(`/questions/detail?slug=${q.slug}`)}
                  style={{ display: "flex", alignItems: "center", gap: 14, padding: "10px 0", borderBottom: i < bookmarksList.length - 1 ? "1px solid var(--border)" : "none", cursor: "pointer" }}
                >
                  <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, color: "var(--muted-foreground)", minWidth: 24 }}>{String(i + 1)}</span>
                  <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--foreground)", flex: 1 }}>{q.title}</span>
                  <span className={diffClass(q.difficulty)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11 }}>{q.difficulty.charAt(0).toUpperCase() + q.difficulty.slice(1)}</span>
                </div>
              ))}
            </div>
          </>
        )}
      </section>
    </main>
  );
}
