import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { COMPANIES, TOPICS, CORE_TOPIC_SLUGS } from "../data.js";
import StatsCounter from "../components/StatsCounter.jsx";

export default function HomePage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");

  const handleSearch = (e) => {
    if (e.key === "Enter" && search.trim()) {
      navigate(`/search?q=${encodeURIComponent(search.trim())}`);
    }
  };

  return (
    <main style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: "clamp(48px, 8vw, 96px)", paddingBottom: "clamp(32px, 5vw, 56px)" }}>
        <h1
          style={{
            fontFamily: "var(--font-dm-sans)",
            fontWeight: 300,
            fontSize: "clamp(52px, 9vw, 104px)",
            letterSpacing: "-0.04em",
            lineHeight: 0.93,
            color: "var(--foreground)",
            margin: 0,
          }}
        >
          DSA
          <br />
          Practice
        </h1>
        <p
          style={{
            fontFamily: "var(--font-dm-sans)",
            fontWeight: 400,
            fontSize: "clamp(14px, 2vw, 16px)",
            color: "var(--muted-foreground)",
            marginTop: 20,
            marginBottom: 32,
            maxWidth: 400,
            lineHeight: 1.6,
          }}
        >
          Systematically practice interview questions by company, topic, and difficulty.
        </p>

        <div style={{ position: "relative", maxWidth: 480 }}>
          <input
            type="text"
            placeholder="Search questions, companies, topics…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={handleSearch}
            style={{
              width: "100%",
              height: 44,
              border: "1px solid var(--border)",
              borderRadius: "var(--radius)",
              backgroundColor: "var(--card)",
              color: "var(--foreground)",
              fontFamily: "var(--font-dm-sans)",
              fontSize: 14,
              padding: "0 16px 0 40px",
              outline: "none",
              transition: "border-color 120ms ease",
            }}
            onFocus={(e) => (e.target.style.borderColor = "var(--accent)")}
            onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
          />
          <span style={{ position: "absolute", left: 14, top: "50%", transform: "translateY(-50%)", color: "var(--muted-foreground)", fontSize: 15, pointerEvents: "none" }}>
            ⌕
          </span>
        </div>

        <div style={{ marginTop: 40, display: "flex", gap: 32, flexWrap: "wrap" }}>
          {[
            { val: "3,430", label: "questions" },
            { val: "737", label: "companies" },
            { val: "24", label: "core topics" },
          ].map(({ val, label }) => (
            <div key={label} style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 18, color: "var(--foreground)", letterSpacing: "-0.02em" }}>
                {val}
              </span>
              <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)" }}>
                {label}
              </span>
            </div>
          ))}
        </div>
        
        <StatsCounter />
      </section>

      <hr className="divider" />

      <section style={{ paddingTop: 48, paddingBottom: 48 }}>
        <div className="home-grid" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "48px 80px", alignItems: "start" }}>
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 24 }}>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.08em", color: "var(--muted-foreground)", textTransform: "uppercase" }}>
                Companies
              </span>
              <button onClick={() => navigate("/companies")} style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--accent)", background: "none", border: "none", cursor: "pointer", padding: 0 }}>
                Browse all →
              </button>
            </div>
            {COMPANIES.slice(0, 6).map((c, i) => (
              <div
                key={c.name}
                className="row-hover"
                onClick={() => navigate(`/companies/${c.slug}`)}
                style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", padding: "10px 0", borderBottom: i < 5 ? "1px solid var(--border)" : "none", cursor: "pointer", gap: 12 }}
              >
                <div style={{ display: "flex", alignItems: "baseline", gap: 14 }}>
                  <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, color: "var(--muted-foreground)", minWidth: 20 }}>{c.rank}</span>
                  <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 15, color: "var(--foreground)" }}>{c.name}</span>
                </div>
                <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{c.count.toLocaleString()}</span>
              </div>
            ))}
          </div>

          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 24 }}>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.08em", color: "var(--muted-foreground)", textTransform: "uppercase" }}>
                Topics
              </span>
              <button onClick={() => navigate("/topics")} style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--accent)", background: "none", border: "none", cursor: "pointer", padding: 0 }}>
                Browse all →
              </button>
            </div>
            {TOPICS.filter(t => CORE_TOPIC_SLUGS.has(t.slug)).slice(0, 6).map((t, i) => (
              <div
                key={t.name}
                className="row-hover"
                onClick={() => navigate(`/topics/${t.slug}`)}
                style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", padding: "10px 0", borderBottom: i < 5 ? "1px solid var(--border)" : "none", cursor: "pointer" }}
              >
                <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 15, color: "var(--foreground)" }}>{t.name}</span>
                <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{t.count.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <hr className="divider" />

      <section style={{ padding: "28px 0 56px", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 16 }}>
        <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)" }}>
          Your progress stays on this device.
        </span>
        <button
          onClick={() => navigate("/practice")}
          style={{
            fontFamily: "var(--font-dm-sans)",
            fontWeight: 500,
            fontSize: 14,
            color: "var(--primary-foreground)",
            backgroundColor: "var(--accent)",
            border: "none",
            borderRadius: "var(--radius)",
            padding: "10px 20px",
            cursor: "pointer",
            letterSpacing: "-0.01em",
          }}
        >
          Start practice session →
        </button>
      </section>

      <style>{`
        @media (max-width: 640px) {
          .home-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </main>
  );
}
