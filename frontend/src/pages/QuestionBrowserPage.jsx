import { useState, useEffect, useRef } from "react";
import { useSearchParams } from "react-router-dom";
import { getQuestions } from "../api.js";
import QuestionTable from "../components/QuestionTable.jsx";
import Pagination from "../components/Pagination.jsx";

export default function QuestionBrowserPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  const filter = searchParams.get("difficulty") || "All";
  const search = searchParams.get("search") || "";
  const page = parseInt(searchParams.get("page")) || 1;

  // We maintain a local input state for the search box so it feels responsive,
  // but only sync it to the URL (which drives the fetch) after a debounce.
  const [searchInput, setSearchInput] = useState(search);
  
  const [questions, setQuestions] = useState([]);
  const [pagination, setPagination] = useState({ total: 0, totalPages: 0 });
  const [isLoading, setIsLoading] = useState(true);

  // Sync external URL changes back to local input (e.g. Back button)
  useEffect(() => {
    setSearchInput(search);
  }, [search]);

  // Debounce search input -> URL param
  useEffect(() => {
    const handler = setTimeout(() => {
      if (searchInput !== search) {
        setSearchParams((prev) => {
          if (searchInput) prev.set("search", searchInput);
          else prev.delete("search");
          prev.set("page", "1"); // Reset page on search change
          return prev;
        }, { replace: true }); // Use replace to avoid filling history with every keystroke
      }
    }, 300);
    return () => clearTimeout(handler);
  }, [searchInput, search, setSearchParams]);

  useEffect(() => {
    const fetchQuestions = async () => {
      setIsLoading(true);
      try {
        const params = { limit: 50, page };
        if (filter !== "All") params.difficulty = filter.toLowerCase();
        if (search) params.search = search;
        
        const data = await getQuestions(params);
        setQuestions(data.items || []);
        setPagination({ total: data.total || 0, totalPages: data.total_pages || 0 });
      } catch (err) {
        console.error("Failed to fetch questions", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchQuestions();
  }, [filter, search, page]);

  const handleFilterChange = (newFilter) => {
    setSearchParams((prev) => {
      if (newFilter === "All") prev.delete("difficulty");
      else prev.set("difficulty", newFilter);
      prev.set("page", "1"); // Reset page on filter change
      return prev;
    });
  };

  const handlePageChange = (newPage) => {
    setSearchParams((prev) => {
      prev.set("page", newPage.toString());
      return prev;
    });
  };

  return (
    <main style={{ maxWidth: 1000, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", flexWrap: "wrap", gap: 16, marginBottom: 24 }}>
          <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(32px, 5vw, 52px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: 0 }}>Questions</h1>
          <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--muted-foreground)" }}>{pagination.total.toLocaleString()} total</span>
        </div>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
          <div style={{ position: "relative", flex: "1 1 240px" }}>
            <input
              type="text"
              placeholder="Search questions…"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              style={{ width: "100%", height: 40, border: "1px solid var(--border)", borderRadius: "var(--radius)", backgroundColor: "var(--card)", color: "var(--foreground)", fontFamily: "var(--font-dm-sans)", fontSize: 14, padding: "0 12px 0 36px", outline: "none", transition: "border-color 120ms ease" }}
              onFocus={(e) => (e.target.style.borderColor = "var(--accent)")}
              onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
            />
            <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "var(--muted-foreground)", fontSize: 15, pointerEvents: "none" }}>⌕</span>
          </div>
          <div style={{ display: "flex", gap: 0, border: "1px solid var(--border)", borderRadius: "var(--radius)", overflow: "hidden" }}>
            {["All", "Easy", "Medium", "Hard"].map((f) => (
              <button key={f} onClick={() => handleFilterChange(f)} style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: filter === f ? "var(--primary-foreground)" : "var(--muted-foreground)", backgroundColor: filter === f ? "var(--accent)" : "transparent", border: "none", borderRight: f !== "Hard" ? "1px solid var(--border)" : "none", cursor: "pointer", padding: "8px 14px", transition: "background-color 120ms ease, color 120ms ease" }}>
                {f}
              </button>
            ))}
          </div>
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
