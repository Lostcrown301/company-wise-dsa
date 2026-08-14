import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCompanies, getTopics } from "../api.js";

function Dropdown({ label, value, options, onChange }) {
  const [open, setOpen] = useState(false);
  const displayValue = options.find(o => o.value === value)?.label || "Select...";

  return (
    <div style={{ marginBottom: 24 }}>
      <label style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--muted-foreground)", display: "block", marginBottom: 8 }}>{label}</label>
      <div style={{ position: "relative" }}>
        <button
          onClick={() => setOpen((v) => !v)}
          style={{ width: "100%", height: 44, border: "1px solid var(--border)", borderRadius: "var(--radius)", backgroundColor: "var(--card)", color: "var(--foreground)", fontFamily: "var(--font-dm-sans)", fontSize: 14, padding: "0 40px 0 14px", textAlign: "left", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "space-between" }}
        >
          <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{displayValue}</span>
          <span style={{ color: "var(--muted-foreground)", fontSize: 11, flexShrink: 0 }}>▾</span>
        </button>
        {open && (
          <div style={{ position: "absolute", top: "calc(100% + 4px)", left: 0, right: 0, zIndex: 20, backgroundColor: "var(--card)", border: "1px solid var(--border)", borderRadius: "var(--radius)", boxShadow: "0 4px 16px rgba(0,0,0,0.08)", maxHeight: 200, overflowY: "auto" }}>
            {options.map((opt) => (
              <button key={opt.value} onClick={() => { onChange(opt.value); setOpen(false); }} style={{ display: "block", width: "100%", padding: "10px 14px", textAlign: "left", backgroundColor: opt.value === value ? "var(--muted)" : "transparent", border: "none", fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--foreground)", cursor: "pointer" }}>
                {opt.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function PracticeSetupPage() {
  const navigate = useNavigate();
  const [company, setCompany] = useState("");
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [count, setCount] = useState(10);

  const [companyOptions, setCompanyOptions] = useState([{ value: "", label: "All companies" }]);
  const [topicOptions, setTopicOptions] = useState([{ value: "", label: "All topics" }]);

  useEffect(() => {
    getCompanies().then(data => {
      setCompanyOptions([
        { value: "", label: "All companies" },
        ...data.map(c => ({ value: c.slug, label: c.name }))
      ]);
    }).catch(console.error);

    getTopics().then(data => {
      setTopicOptions([
        { value: "", label: "All topics" },
        ...data.map(t => ({ value: t.slug, label: t.name }))
      ]);
    }).catch(console.error);
  }, []);

  const difficultyOptions = [
    { value: "", label: "Any difficulty" },
    { value: "easy", label: "Easy" },
    { value: "medium", label: "Medium" },
    { value: "hard", label: "Hard" }
  ];

  const handleStart = () => {
    const params = new URLSearchParams();
    if (company) params.set("company", company);
    if (topic) params.set("topic", topic);
    if (difficulty) params.set("difficulty", difficulty);
    params.set("limit", count.toString());
    navigate(`/practice/session?${params.toString()}`);
  };

  return (
    <main style={{ maxWidth: 480, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 64 }}>
        <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(28px, 5vw, 44px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: "0 0 8px" }}>Practice</h1>
        <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--muted-foreground)", margin: "0 0 40px", lineHeight: 1.6 }}>Build a focused session from your criteria.</p>

        <Dropdown label="Company" value={company} options={companyOptions} onChange={setCompany} />
        <Dropdown label="Topic" value={topic} options={topicOptions} onChange={setTopic} />
        <Dropdown label="Difficulty" value={difficulty} options={difficultyOptions} onChange={setDifficulty} />

        <div style={{ marginBottom: 40 }}>
          <label style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--muted-foreground)", display: "block", marginBottom: 8 }}>Questions</label>
          <div style={{ display: "flex", gap: 8 }}>
            {[5, 10, 15, 20].map((n) => (
              <button key={n} onClick={() => setCount(n)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: 14, color: count === n ? "var(--primary-foreground)" : "var(--muted-foreground)", backgroundColor: count === n ? "var(--accent)" : "transparent", border: "1px solid var(--border)", borderRadius: "var(--radius)", padding: "8px 16px", cursor: "pointer", transition: "background-color 120ms ease, color 120ms ease" }}>
                {n}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleStart}
          style={{ width: "100%", height: 48, fontFamily: "var(--font-dm-sans)", fontWeight: 500, fontSize: 15, color: "var(--primary-foreground)", backgroundColor: "var(--accent)", border: "none", borderRadius: "var(--radius)", cursor: "pointer", letterSpacing: "-0.01em" }}
        >
          Start session →
        </button>
      </section>
    </main>
  );
}
