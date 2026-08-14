import React from "react";
import { useLocation } from "react-router-dom";

export default function Footer() {
  const location = useLocation();
  const path = location.pathname;

  if (path === "/practice/session") {
    return null;
  }

  const isFull = path === "/";

  return (
    <footer style={{ 
      borderTop: "1px solid var(--border)", 
      padding: isFull ? "48px 24px 32px" : "24px", 
      marginTop: "auto",
      backgroundColor: "var(--background)"
    }}>
      {isFull && (
        <div style={{ 
          maxWidth: 1000, 
          margin: "0 auto", 
          display: "grid", 
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", 
          gap: 64, 
          marginBottom: 64 
        }}>
          
          {/* DATA SOURCES SECTION */}
          <div>
            <h3 style={{ 
              fontFamily: "var(--font-dm-mono)", 
              fontSize: 11, 
              letterSpacing: "0.06em", 
              color: "var(--muted-foreground)", 
              textTransform: "uppercase", 
              marginBottom: 24,
              fontWeight: 500
            }}>
              Data Sources
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              {[
                { repo: "krishnadey30/LeetCode-Questions-CompanyWise", url: "https://github.com/krishnadey30/leetcode-questions-companywise", license: "No license file published" },
                { repo: "snehasishroy/leetcode-companywise-interview-questions", url: "https://github.com/snehasishroy/leetcode-companywise-interview-questions", license: "No license file published" },
                { repo: "ADHIL48/Leetcode-Companys-wise-Question-and-Solution", url: "https://github.com/ADHIL48/Leetcode-Companys-wise-Question-and-Solution", license: "No license file published" },
                { repo: "liquidslr/leetcode-company-wise-problems", url: "https://github.com/liquidslr/leetcode-company-wise-problems", license: "No license file published" },
                { repo: "hxu296/leetcode-company-wise-problems-2022", url: "https://github.com/hxu296/leetcode-company-wise-problems-2022", license: "MIT" }
              ].map((source, idx) => (
                <div key={idx}>
                  <div style={{ fontFamily: "var(--font-dm-mono)", fontSize: 13, color: "var(--foreground)", marginBottom: 4, wordBreak: "break-all" }}>
                    <a 
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: "inherit", textDecoration: "none", transition: "color 150ms ease" }}
                      onMouseEnter={(e) => e.currentTarget.style.color = "var(--accent)"}
                      onMouseLeave={(e) => e.currentTarget.style.color = "inherit"}
                    >
                      {source.repo} <span style={{ fontSize: "0.85em", opacity: 0.7 }}>↗</span>
                    </a>
                  </div>
                  <div style={{ fontFamily: "var(--font-dm-sans)", fontSize: 12, color: "var(--muted-foreground)" }}>
                    {source.license}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* SCOPE SECTION */}
          <div>
            <h3 style={{ 
              fontFamily: "var(--font-dm-mono)", 
              fontSize: 11, 
              letterSpacing: "0.06em", 
              color: "var(--muted-foreground)", 
              textTransform: "uppercase", 
              marginBottom: 24,
              fontWeight: 500
            }}>
              Scope
            </h3>
            <ul style={{ 
              listStyle: "none", 
              padding: 0, 
              margin: 0, 
              display: "flex", 
              flexDirection: "column", 
              gap: 16 
            }}>
              {[
                // "Free problems only - premium problems are filtered out before build.",
                "Titles, difficulty, and link only. No statements, tests, or editorials.",
                "Frequency is a merged relative signal, not an official LeetCode statistic.",
                "Not affiliated with LeetCode or any company listed.",
                "Dataset last updated · Aug 15, 2026"
              ].map((text, idx) => (
                <li key={idx} style={{ 
                  fontFamily: "var(--font-dm-sans)", 
                  fontSize: 13, 
                  color: "var(--muted-foreground)",
                  lineHeight: 1.5
                }}>
                  {text}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* BOTTOM BAR */}
      <div style={{ 
        maxWidth: 1000, 
        margin: "0 auto", 
        borderTop: isFull ? "1px solid var(--border)" : "none", 
        paddingTop: isFull ? 32 : 0, 
        display: "flex", 
        justifyContent: "space-between",
        alignItems: "center",
        flexWrap: "wrap",
        gap: 16
      }}>
        <div style={{ 
          fontFamily: "var(--font-dm-mono)", 
          fontSize: 11, 
          letterSpacing: "0.06em", 
          color: "var(--muted-foreground)", 
          textTransform: "uppercase" 
        }}>
          © 2026 ASHUTOSH SHUKLA
        </div>
        <div style={{ 
          fontFamily: "var(--font-dm-mono)", 
          fontSize: 11, 
          letterSpacing: "0.06em", 
          color: "var(--muted-foreground)", 
          textTransform: "uppercase" 
        }}>
          DEVELOPED BY <a 
            href="https://ashutosh-shukla-portfolio.vercel.app/" 
            target="_blank" 
            rel="noopener noreferrer" 
            style={{ color: "var(--foreground)", textDecoration: "none", borderBottom: "1px solid var(--accent)", transition: "color 150ms ease" }}
            onMouseEnter={(e) => e.currentTarget.style.color = "var(--accent)"}
            onMouseLeave={(e) => e.currentTarget.style.color = "var(--foreground)"}
          >ASHUTOSH</a> USING ANTIGRAVITY
        </div>
      </div>
    </footer>
  );
}
