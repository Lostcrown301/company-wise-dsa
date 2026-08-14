import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const ProgressContext = createContext();

const LOCAL_STORAGE_KEY = "dsa_progress";

const DEFAULT_PROGRESS = {
  version: 2,
  solved: {},
  bookmarked: [],
  notes: {}
};

export function ProgressProvider({ children }) {
  const [progress, setProgress] = useState(() => {
    try {
      const stored = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (!stored) return DEFAULT_PROGRESS;
      let parsed = JSON.parse(stored);
      
      // Migrate V1 to V2
      if (!parsed.version || parsed.version === 1 || Array.isArray(parsed.solved)) {
        const migratedSolved = {};
        const now = new Date().toISOString();
        if (Array.isArray(parsed.solved)) {
          parsed.solved.forEach(slug => {
            migratedSolved[slug] = { solvedAt: now };
          });
        }
        parsed = {
          ...DEFAULT_PROGRESS,
          ...parsed,
          version: 2,
          solved: migratedSolved
        };
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(parsed));
      }
      
      // Ensure all keys exist
      return { ...DEFAULT_PROGRESS, ...parsed, version: 2 };
    } catch (e) {
      console.error("Failed to parse progress from local storage", e);
      return DEFAULT_PROGRESS;
    }
  });

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  const toggleSolved = useCallback((slug) => {
    setProgress(prev => {
      const nextSolved = { ...prev.solved };
      if (nextSolved[slug]) {
        delete nextSolved[slug];
      } else {
        nextSolved[slug] = { solvedAt: new Date().toISOString() };
      }
      return { ...prev, solved: nextSolved };
    });
  }, []);

  const toggleBookmarked = useCallback((slug) => {
    setProgress(prev => {
      const isBookmarked = prev.bookmarked.includes(slug);
      const nextBookmarked = isBookmarked 
        ? prev.bookmarked.filter(s => s !== slug)
        : [...prev.bookmarked, slug];
      return { ...prev, bookmarked: nextBookmarked };
    });
  }, []);

  const saveNote = useCallback((slug, note) => {
    setProgress(prev => {
      const nextNotes = { ...prev.notes };
      if (!note || note.trim().length === 0) {
        delete nextNotes[slug];
      } else {
        nextNotes[slug] = note;
      }
      return { ...prev, notes: nextNotes };
    });
  }, []);

  const isSolved = useCallback((slug) => !!progress.solved[slug], [progress.solved]);
  const isBookmarked = useCallback((slug) => progress.bookmarked.includes(slug), [progress.bookmarked]);
  const getNote = useCallback((slug) => progress.notes[slug] || "", [progress.notes]);

  const exportProgress = useCallback(() => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
      app: "DSA Practice",
      exportedAt: new Date().toISOString(),
      ...progress
    }, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "dsa_progress.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  }, [progress]);

  const importProgress = useCallback((data, mode) => {
    try {
      if (mode === "replace") {
        setProgress({ 
          version: 2, 
          solved: data.solved || {}, 
          bookmarked: data.bookmarked || [], 
          notes: data.notes || {} 
        });
      } else if (mode === "merge") {
        setProgress(prev => {
          const mergedSolved = { ...prev.solved, ...(data.solved || {}) };
          const mergedBookmarked = Array.from(new Set([...prev.bookmarked, ...(data.bookmarked || [])]));
          const mergedNotes = { ...prev.notes, ...(data.notes || {}) };
          return {
            version: 2,
            solved: mergedSolved,
            bookmarked: mergedBookmarked,
            notes: mergedNotes
          };
        });
      }
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  const resetProgress = useCallback(() => {
    setProgress(DEFAULT_PROGRESS);
    localStorage.removeItem(LOCAL_STORAGE_KEY);
  }, []);

  const value = {
    progress,
    toggleSolved,
    toggleBookmarked,
    saveNote,
    isSolved,
    isBookmarked,
    getNote,
    exportProgress,
    importProgress,
    resetProgress
  };

  return (
    <ProgressContext.Provider value={value}>
      {children}
    </ProgressContext.Provider>
  );
}

export function useProgress() {
  const context = useContext(ProgressContext);
  if (!context) {
    throw new Error("useProgress must be used within a ProgressProvider");
  }
  return context;
}
