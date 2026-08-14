import { useState, useEffect } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";
import { getCompanies, getTopics, getQuestions } from "../api.js";
import QuestionTable from "../components/QuestionTable.jsx";

export default function GlobalSearchPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const query = searchParams.get("q") || "";

  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState({ companies: [], topics: [], questions: [] });
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!query) {
      setLoading(false);
      setResults({ companies: [], topics: [], questions: [] });
      return;
    }

    async function fetchAll() {
      setLoading(true);
      setError(null);
      try {
        const [companies, topics, questionsData] = await Promise.all([
          getCompanies(query),
          getTopics(query),
          getQuestions({ search: query, limit: 50 })
        ]);
        
        setResults({
          companies: companies || [],
          topics: topics || [],
          questions: questionsData.items || []
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchAll();
  }, [query]);

  const hasResults = results.companies.length > 0 || results.topics.length > 0 || results.questions.length > 0;

  return (
    <main style={{ maxWidth: 1000, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 32 }}>
        <button onClick={() => navigate(-1)} style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)", background: "none", border: "none", cursor: "pointer", padding: 0, marginBottom: 20, display: "block" }}>
          ← Back
        </button>
        <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(32px, 5vw, 52px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: "0 0 8px" }}>
          Search Results
        </h1>
        <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 15, color: "var(--muted-foreground)", margin: 0 }}>
          Showing results for "{query}"
        </p>
      </section>

      {loading ? (
        <div style={{ padding: "64px 0", textAlign: "center" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>Searching...</p>
        </div>
      ) : error ? (
        <div style={{ padding: "64px 0", textAlign: "center" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "#A63325" }}>{error}</p>
        </div>
      ) : !hasResults ? (
        <div style={{ padding: "64px 0", textAlign: "center" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>No results found.</p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 56, paddingBottom: 64 }}>
          {results.companies.length > 0 && (
            <div>
              <h2 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 18, color: "var(--foreground)", marginBottom: 16 }}>Companies</h2>
              <div style={{ borderTop: "1px solid var(--border)" }}>
                {results.companies.map((c, i) => (
                  <Link
                    key={c.slug}
                    to={`/companies/detail?slug=${c.slug}`}
                    className="row-hover"
                    style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "13px 0", borderBottom: i < results.companies.length - 1 ? "1px solid var(--border)" : "none", textDecoration: "none" }}
                  >
                    <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 15, color: "var(--foreground)" }}>{c.name}</span>
                    <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{c.question_count?.toLocaleString() || 0}</span>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {results.topics.length > 0 && (
            <div>
              <h2 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 18, color: "var(--foreground)", marginBottom: 16 }}>Topics</h2>
              <div style={{ borderTop: "1px solid var(--border)" }}>
                {results.topics.map((t, i) => (
                  <Link
                    key={t.slug}
                    to={`/topics/detail?slug=${t.slug}`}
                    className="row-hover"
                    style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "14px 0", borderBottom: i < results.topics.length - 1 ? "1px solid var(--border)" : "none", textDecoration: "none" }}
                  >
                    <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 15, color: "var(--foreground)" }}>{t.name}</span>
                    <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{t.question_count?.toLocaleString() || 0}</span>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {results.questions.length > 0 && (
            <div>
              <h2 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 18, color: "var(--foreground)", marginBottom: 16 }}>Questions</h2>
              <QuestionTable questions={results.questions} startIndex={1} />
            </div>
          )}
        </div>
      )}
    </main>
  );
}
