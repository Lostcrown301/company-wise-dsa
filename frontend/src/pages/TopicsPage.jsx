import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getTopics } from "../api.js";

export default function TopicsPage() {
  const navigate = useNavigate();
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getTopics();
        setTopics(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", flexWrap: "wrap", gap: 16, marginBottom: 32 }}>
          <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(32px, 5vw, 52px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: 0 }}>
            Topics
          </h1>
          {!loading && !error && (
            <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{topics.length} total</span>
          )}
        </div>
      </section>

      {loading ? (
        <div style={{ padding: "64px 0", textAlign: "center" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>Loading topics...</p>
        </div>
      ) : error ? (
        <div style={{ padding: "64px 0", textAlign: "center" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "#A63325" }}>{error}</p>
        </div>
      ) : (
        <div style={{ borderTop: "1px solid var(--border)" }}>
          {topics.map((t, i) => {
            const count = t.question_count || 0;
            // Assuming 1140 is roughly the max for Array or we can calculate it dynamically
            // But we'll just use 1140 as a visual max based on the original design
            const pct = Math.min((count / 1140) * 100, 100);
            return (
              <div
                key={t.id || t.slug}
                className="row-hover"
                onClick={() => navigate(`/topics/${t.slug}`)}
                style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "14px 0", borderBottom: i < topics.length - 1 ? "1px solid var(--border)" : "none", cursor: "pointer" }}
              >
                <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 15, color: "var(--foreground)" }}>{t.name}</span>
                <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
                  <div style={{ width: 80, height: 2, backgroundColor: "var(--border)", borderRadius: 1, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: `${pct}%`, backgroundColor: "var(--accent)", opacity: 0.5, borderRadius: 1 }} />
                  </div>
                  <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)", minWidth: 40, textAlign: "right" }}>{count.toLocaleString()}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </main>
  );
}
