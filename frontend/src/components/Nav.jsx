import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

const NAV_ITEMS = [
  { id: "companies", path: "/companies", label: "Companies" },
  { id: "topics", path: "/topics", label: "Topics" },
  { id: "practice-setup", path: "/practice", label: "Practice" },
];

export default function Nav({ theme, setTheme }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  const isCurrent = (path) => location.pathname.startsWith(path);

  return (
    <header
      style={{
        borderBottom: "1px solid var(--border)",
        backgroundColor: "var(--background)",
        position: "sticky",
        top: 0,
        zIndex: 50,
      }}
    >
      <div
        style={{
          maxWidth: 1200,
          margin: "0 auto",
          padding: "0 24px",
          height: 56,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Link
          to="/"
          style={{
            fontFamily: "var(--font-dm-sans)",
            fontWeight: 600,
            fontSize: 15,
            letterSpacing: "-0.02em",
            color: "var(--foreground)",
            textDecoration: "none",
          }}
        >
          DSA Practice
        </Link>

        <nav style={{ display: "flex", alignItems: "center", gap: 32 }} className="nav-desktop">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.id}
              to={item.path}
              style={{
                fontFamily: "var(--font-dm-sans)",
                fontWeight: isCurrent(item.path) ? 500 : 400,
                fontSize: 14,
                color: isCurrent(item.path) ? "var(--accent)" : "var(--muted-foreground)",
                textDecoration: "none",
                transition: "color 120ms ease",
              }}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <Link
            to="/progress"
            className="nav-desktop"
            style={{
              fontFamily: "var(--font-dm-sans)",
              fontWeight: 400,
              fontSize: 14,
              color: isCurrent("/progress") ? "var(--accent)" : "var(--muted-foreground)",
              textDecoration: "none",
            }}
          >
            Progress
          </Link>
          <Link
            to="/settings"
            className="nav-desktop"
            style={{
              fontSize: 16,
              color: "var(--muted-foreground)",
              textDecoration: "none",
              lineHeight: 1,
            }}
            title="Settings"
          >
            ·
            ·
            ·
          </Link>
          <button
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            style={{
              width: 32,
              height: 32,
              border: "1px solid var(--border)",
              borderRadius: "var(--radius)",
              background: "var(--muted)",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 14,
              color: "var(--muted-foreground)",
            }}
          >
            {theme === "light" ? "◑" : "○"}
          </button>
          <button
            onClick={() => setMobileOpen((v) => !v)}
            className="nav-mobile"
            style={{
              width: 32,
              height: 32,
              border: "1px solid var(--border)",
              borderRadius: "var(--radius)",
              background: "var(--muted)",
              cursor: "pointer",
              display: "none",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 14,
              color: "var(--foreground)",
            }}
          >
            ☰
          </button>
        </div>
      </div>

      {mobileOpen && (
        <div
          style={{
            borderTop: "1px solid var(--border)",
            backgroundColor: "var(--background)",
            padding: "8px 24px 16px",
          }}
        >
          {[...NAV_ITEMS, { id: "progress", path: "/progress", label: "Progress" }, { id: "settings", path: "/settings", label: "Settings" }].map((item) => (
            <Link
              key={item.id}
              to={item.path}
              onClick={() => setMobileOpen(false)}
              style={{
                fontFamily: "var(--font-dm-sans)",
                fontWeight: isCurrent(item.path) ? 500 : 400,
                fontSize: 15,
                color: isCurrent(item.path) ? "var(--accent)" : "var(--foreground)",
                textDecoration: "none",
                borderBottom: "1px solid var(--border)",
                padding: "11px 0",
                display: "block",
              }}
            >
              {item.label}
            </Link>
          ))}
        </div>
      )}

      <style>{`
        @media (max-width: 640px) {
          .nav-desktop { display: none !important; }
          .nav-mobile { display: flex !important; }
        }
      `}</style>
    </header>
  );
}
