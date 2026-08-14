import { useState, useRef } from "react";
import { useProgress } from "../context/ProgressContext.jsx";

export default function SettingsPage({ theme, setTheme }) {
  const [appearance, setAppearance] = useState(theme);
  const { exportProgress, importProgress, resetProgress } = useProgress();
  const fileInputRef = useRef(null);

  const handleAppearance = (val) => {
    setAppearance(val);
    if (val !== "system") setTheme(val);
    else {
      // Switch back to system implies removing forced theme and triggering App.jsx logic
      setTheme("system");
    }
  };

  const handleExport = () => {
    exportProgress();
  };

  const handleImportClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const data = JSON.parse(event.target.result);
        if (data.version !== 2) {
          alert("Invalid file format: Expected version 2 progress data.");
          return;
        }

        if (window.confirm("Are you sure you want to replace all your current progress with this imported data? This cannot be undone.")) {
          const success = importProgress(data, "replace");
          if (success) {
            alert("Progress imported successfully.");
          } else {
            alert("Failed to import progress.");
          }
        }
      } catch (err) {
        alert("Invalid JSON file.");
        console.error(err);
      } finally {
        e.target.value = null; // reset input
      }
    };
    reader.readAsText(file);
  };

  const handleReset = () => {
    if (window.confirm("Are you sure you want to permanently delete all your progress? This cannot be undone.")) {
      resetProgress();
      alert("Progress has been reset.");
    }
  };

  function Radio({ val, label }) {
    return (
      <label style={{ display: "flex", alignItems: "center", gap: 12, padding: "11px 0", cursor: "pointer", borderBottom: "1px solid var(--border)" }}>
        <div style={{ width: 16, height: 16, borderRadius: "50%", border: `1.5px solid ${appearance === val ? "var(--accent)" : "var(--border)"}`, backgroundColor: "transparent", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, transition: "border-color 120ms" }}>
          {appearance === val && <div style={{ width: 7, height: 7, borderRadius: "50%", backgroundColor: "var(--accent)" }} />}
        </div>
        <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--foreground)" }}>{label}</span>
        <input type="radio" value={val} checked={appearance === val} onChange={() => handleAppearance(val)} style={{ display: "none" }} />
      </label>
    );
  }

  return (
    <main style={{ maxWidth: 480, margin: "0 auto", padding: "0 24px" }}>
      <section style={{ paddingTop: 56, paddingBottom: 64 }}>
        <h1 style={{ fontFamily: "var(--font-dm-sans)", fontWeight: 300, fontSize: "clamp(28px, 5vw, 44px)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: "0 0 48px" }}>Settings</h1>

        <div style={{ marginBottom: 48 }}>
          <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--muted-foreground)", display: "block", marginBottom: 4 }}>Appearance</span>
          <div style={{ borderTop: "1px solid var(--border)" }}>
            <Radio val="light" label="Light" />
            <Radio val="dark" label="Dark" />
            <Radio val="system" label="System" />
          </div>
        </div>

        <div style={{ marginBottom: 40 }}>
          <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 11, letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--muted-foreground)", display: "block", marginBottom: 4 }}>Data</span>
          <div style={{ borderTop: "1px solid var(--border)" }}>
            
            <div onClick={handleExport} className="row-hover" style={{ padding: "13px 0", borderBottom: "1px solid var(--border)", cursor: "pointer" }}>
              <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--foreground)", marginBottom: 2 }}>Export progress</div>
              <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 12, color: "var(--muted-foreground)" }}>Download a JSON file of your solved questions and notes.</div>
            </div>

            <div onClick={handleImportClick} className="row-hover" style={{ padding: "13px 0", borderBottom: "1px solid var(--border)", cursor: "pointer" }}>
              <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "var(--foreground)", marginBottom: 2 }}>Import progress</div>
              <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 12, color: "var(--muted-foreground)" }}>Restore from a previously exported file.</div>
              <input 
                type="file" 
                accept=".json" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                style={{ display: "none" }} 
              />
            </div>

            <div onClick={handleReset} className="row-hover" style={{ padding: "13px 0", cursor: "pointer" }}>
              <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 14, color: "#A63325", marginBottom: 2 }}>Reset progress</div>
              <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 12, color: "var(--muted-foreground)" }}>Permanently clear all local data.</div>
            </div>
          </div>
        </div>

        <div style={{ padding: "14px 16px", border: "1px solid var(--border)", borderRadius: "var(--radius)", backgroundColor: "var(--muted)" }}>
          <p style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)", margin: 0, lineHeight: 1.6 }}>
            Your progress is stored locally in this browser. It is never sent to any server — export it to keep a copy.
          </p>
        </div>
      </section>
    </main>
  );
}
