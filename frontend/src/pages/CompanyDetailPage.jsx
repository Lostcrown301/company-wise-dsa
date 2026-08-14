import { useState, useEffect } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { getCompanyDetails, getQuestions } from "../api.js";
import QuestionTable from "../components/QuestionTable.jsx";
import Pagination from "../components/Pagination.jsx";
import { diffClass } from "../components/utils.js";

export default function CompanyDetailPage() {
  const navigate = useNavigate();
  const { slug } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const filter = searchParams.get("difficulty") || "All";
  const page = parseInt(searchParams.get("page")) || 1;

  const [company, setCompany] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [pagination, setPagination] = useState({ total: 0, totalPages: 0 });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!slug) {
      navigate("/companies");
      return;
    }

    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [compData, qData] = await Promise.all([
          getCompanyDetails(slug),
          getQuestions({ 
            company: slug, 
            limit: 50, 
            page, 
            difficulty: filter === "All" ? undefined : filter.toLowerCase() 
          })
        ]);
        setCompany(compData);
        setQuestions(qData.items || []);
        setPagination({ total: qData.total || 0, totalPages: qData.total_pages || 0 });
      } catch (err) {
        console.error("Failed to fetch company details", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [slug, filter, page, navigate]);

  const handleFilterChange = (newFilter) => {
    setSearchParams((prev) => {
      if (newFilter === "All") prev.delete("difficulty");
      else prev.set("difficulty", newFilter);
      prev.set("page", "1"); // Reset to page 1 on filter change
      return prev;
    });
  };

  const handlePageChange = (newPage) => {
    setSearchParams((prev) => {
      prev.set("page", newPage.toString());
      return prev;
    });
  };

  if (isLoading && !company) {
    return (
      <main style={{ maxWidth: 900, margin: "0 auto", padding: "0 24px" }}>
        <section style={{ paddingTop: 40, paddingBottom: 32 }}>
          <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>Loading...</div>
        </section>
      </main>
    );
  }

  if (!company) return null;

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 40, paddingBottom: 32 }}>
        <button onClick={() => navigate("/companies")} style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)", background: "none", border: "none", cursor: "pointer", padding: 0, marginBottom: 20, display: "block" }}>
          ← Companies
        </button>
        <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(28px, 5vw, 48px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: "0 0 4px" }}>
          {company.name}
        </h1>
        <p style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)", margin: "0 0 24px" }}>
          {pagination.total.toLocaleString()} questions
        </p>

        <div style={{ display: "flex", gap: 28, flexWrap: "wrap", marginBottom: 28 }}>
          {[{ label: "Easy", count: company.difficulty?.easy || 0 }, { label: "Medium", count: company.difficulty?.medium || 0 }, { label: "Hard", count: company.difficulty?.hard || 0 }].map(({ label, count }) => (
            <div key={label} style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
              <span className={diffClass(label)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 12 }}>{label}</span>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{count.toLocaleString()}</span>
            </div>
          ))}
        </div>

        <div style={{ display: "flex", gap: 0, borderBottom: "1px solid var(--border)" }}>
          {["All", "Easy", "Medium", "Hard"].map((f) => (
            <button
              key={f}
              onClick={() => handleFilterChange(f)}
              style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, fontWeight: filter === f ? 500 : 400, color: filter === f ? "var(--accent)" : "var(--muted-foreground)", background: "none", border: "none", borderBottom: filter === f ? "2px solid var(--accent)" : "2px solid transparent", cursor: "pointer", padding: "8px 16px", marginBottom: -1, transition: "color 120ms ease" }}
            >
              {f}
            </button>
          ))}
        </div>
      </section>

      {questions.length === 0 ? (
        <div style={{ padding: "64px 0", textAlign: "center" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)" }}>No questions found.</p>
        </div>
      ) : (
        <>
          <div style={{ opacity: isLoading ? 0.5 : 1, transition: "opacity 200ms" }}>
            <QuestionTable questions={questions} startIndex={(page - 1) * 50 + 1} />
          </div>
          <Pagination page={page} totalPages={pagination.totalPages} onPageChange={handlePageChange} />
        </>
      )}
      <div style={{ height: 64 }} />
    </main>
  );
}
