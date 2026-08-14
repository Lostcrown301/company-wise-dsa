import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Nav from "./components/Nav.jsx";
import HomePage from "./pages/HomePage.jsx";
import CompaniesPage from "./pages/CompaniesPage.jsx";
import CompanyDetailPage from "./pages/CompanyDetailPage.jsx";
import TopicsPage from "./pages/TopicsPage.jsx";
import TopicDetailPage from "./pages/TopicDetailPage.jsx";
import QuestionBrowserPage from "./pages/QuestionBrowserPage.jsx";
import QuestionDetailPage from "./pages/QuestionDetailPage.jsx";
import PracticeSetupPage from "./pages/PracticeSetupPage.jsx";
import PracticeSessionPage from "./pages/PracticeSessionPage.jsx";
import ProgressPage from "./pages/ProgressPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";
import GlobalSearchPage from "./pages/GlobalSearchPage.jsx";
import Footer from "./components/Footer.jsx";

import { ProgressProvider } from "./context/ProgressContext.jsx";

export default function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("dsa_theme") || "light";
  });

  useEffect(() => {
    localStorage.setItem("dsa_theme", theme);
    
    const root = document.documentElement;
    const applyDark = () => root.classList.add("dark");
    const removeDark = () => root.classList.remove("dark");

    if (theme === "dark") {
      applyDark();
    } else if (theme === "light") {
      removeDark();
    } else if (theme === "system") {
      const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      if (systemPrefersDark) applyDark();
      else removeDark();
    }
  }, [theme]);

  useEffect(() => {
    if (theme !== "system") return;
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleChange = (e) => {
      const root = document.documentElement;
      if (e.matches) root.classList.add("dark");
      else root.classList.remove("dark");
    };
    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, [theme]);

  return (
    <ProgressProvider>
      <Router>
        <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", backgroundColor: "var(--background)" }}>
          <Nav theme={theme} setTheme={setTheme} />
          <div style={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/companies" element={<CompaniesPage />} />
              <Route path="/companies/:slug" element={<CompanyDetailPage />} />
              <Route path="/topics" element={<TopicsPage />} />
              <Route path="/topics/:slug" element={<TopicDetailPage />} />
              <Route path="/questions" element={<QuestionBrowserPage />} />
              <Route path="/questions/detail" element={<QuestionDetailPage />} />
              <Route path="/practice" element={<PracticeSetupPage />} />
              <Route path="/practice/session" element={<PracticeSessionPage />} />
              <Route path="/progress" element={<ProgressPage />} />
              <Route path="/settings" element={<SettingsPage theme={theme} setTheme={setTheme} />} />
              <Route path="/search" element={<GlobalSearchPage />} />
            </Routes>
          </div>
          <Footer />
        </div>
      </Router>
    </ProgressProvider>
  );
}
