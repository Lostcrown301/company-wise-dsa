import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getTopics } from "../api.js";
import { CORE_TOPIC_SLUGS } from "../data.js";

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

  const coreTopics = topics.filter(t => CORE_TOPIC_SLUGS.has(t.slug));
  const specializedTopics = topics.filter(t => !CORE_TOPIC_SLUGS.has(t.slug));

  // Max count for the bar chart scaling — use largest core topic count
  const maxCount = topics.reduce((m, t) => Math.max(m, t.question_count || 0), 1);

  const TopicRow = ({ t, i, arr }) => {
    const count = t.question_count || 0;
    const pct = Math.min((count / maxCount) * 100, 100);
    return (
      <div
        key={t.id || t.slug}
        className="row-hover"
        onClick={() => navigate(`/topics/${t.slug}`)}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "13px 0",
          borderBottom: i < arr.length - 1 ? "1px solid var(--border)" : "none",
          cursor: "pointer",
        }}
      >
        <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 15, color: "var(--foreground)" }}>
          {t.name}
        </span>
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div style={{ width: 80, height: 2, backgroundColor: "var(--border)", borderRadius: 1, overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${pct}%`, backgroundColor: "var(--accent)", opacity: 0.5, borderRadius: 1 }} />
          </div>
          <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)", minWidth: 40, textAlign: "right" }}>
            {count.toLocaleString()}
          </span>
        </div>
      </div>
    );
  };

  const SectionHeader = ({ label, count }) => (
    <div style={{
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 2,
    }}>
      <span style={{
        fontFamily: "var(--font-dm-mono)",
        fontSize: 11,
        letterSpacing: "0.08em",
        color: "var(--muted-foreground)",
        textTransform: "uppercase",
      }}>
        {label}
      </span>
      {count != null && (
        <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, color: "var(--muted-foreground)" }}>
          {count}
        </span>
      )}
    </div>
  );

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", flexWrap: "wrap", gap: 16, marginBottom: 32 }}>
          <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(32px, 5vw, 52px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: 0 }}>
            Topics
          </h1>
          {!loading && !error && (
            <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>
              {coreTopics.length} core · {specializedTopics.length} specialized
            </span>
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
        <>
          {/* Core Topics */}
          <section style={{ marginBottom: 48 }}>
            <SectionHeader label="Core Topics" count={coreTopics.length} />
            <div style={{ borderTop: "1px solid var(--border)" }}>
              {coreTopics.map((t, i) => (
                <TopicRow key={t.id || t.slug} t={t} i={i} arr={coreTopics} />
              ))}
            </div>
          </section>

          {/* Specialized Topics */}
          {specializedTopics.length > 0 && (
            <section style={{ marginBottom: 64 }}>
              <SectionHeader label="Specialized Topics" count={specializedTopics.length} />
              <div style={{ borderTop: "1px solid var(--border)" }}>
                {specializedTopics.map((t, i) => (
                  <TopicRow key={t.id || t.slug} t={t} i={i} arr={specializedTopics} />
                ))}
              </div>
            </section>
          )}
        </>
      )}
    </main>
  );
}
