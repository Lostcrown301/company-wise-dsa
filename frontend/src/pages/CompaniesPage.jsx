import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCompanies } from "../api.js";

export default function CompaniesPage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);
    return () => clearTimeout(handler);
  }, [search]);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await getCompanies(debouncedSearch);
        setCompanies(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [debouncedSearch]);

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", flexWrap: "wrap", gap: 16, marginBottom: 8 }}>
          <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(32px, 5vw, 52px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: 0 }}>
            Companies
          </h1>
          {!loading && !error && (
            <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{companies.length} total</span>
          )}
        </div>
        <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)", margin: "0 0 28px", lineHeight: 1.6 }}>
          Questions ranked by frequency of appearance in interviews.
        </p>
        <div style={{ position: "relative", maxWidth: 360 }}>
          <input
            type="text"
            placeholder="Search companies…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: "100%", height: 40, border: "1px solid var(--border)", borderRadius: "var(--radius)", backgroundColor: "var(--card)", color: "var(--foreground)", fontFamily: "var(--font-dm-sans)", fontSize: 14, padding: "0 12px 0 36px", outline: "none" }}
            onFocus={(e) => (e.target.style.borderColor = "var(--accent)")}
            onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
          />
          <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "var(--muted-foreground)", fontSize: 15, pointerEvents: "none" }}>⌕</span>
        </div>
      </section>

      <div style={{ display: "grid", gridTemplateColumns: "40px 1fr auto", gap: 16, padding: "0 0 8px", borderBottom: "1px solid var(--border)" }}>
        {["#", "Company", "Questions"].map((h) => (
          <span key={h} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", color: "var(--muted-foreground)", textTransform: "uppercase" }}>{h}</span>
        ))}
      </div>

      {loading ? (
        <div style={{ padding: "64px 0", textAlign: "center" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>Loading companies...</p>
        </div>
      ) : error ? (
        <div style={{ padding: "64px 0", textAlign: "center" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "#A63325" }}>{error}</p>
        </div>
      ) : (
        <>
          {companies.map((c, i) => (
            <div
              key={c.id || c.slug}
              className="row-hover"
              onClick={() => navigate(`/companies/${c.slug}`)}
              style={{ display: "grid", gridTemplateColumns: "40px 1fr auto", gap: 16, padding: "13px 0", borderBottom: i < companies.length - 1 ? "1px solid var(--border)" : "none", cursor: "pointer", alignItems: "center" }}
            >
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12, color: "var(--muted-foreground)" }}>{String(i + 1).padStart(2, '0')}</span>
              <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 15, color: "var(--foreground)" }}>{c.name}</span>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{c.question_count?.toLocaleString() || 0}</span>
            </div>
          ))}

          {companies.length === 0 && (
            <div style={{ padding: "64px 0", textAlign: "center" }}>
              <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>No companies found for "{search}"</p>
            </div>
          )}
        </>
      )}
    </main>
  );
}
