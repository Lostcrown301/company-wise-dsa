import { useState, useEffect } from 'react';
import { getStats } from '../api.js';

function useCountUp(end, duration = 1500) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTimestamp = null;
    let animationFrame;

    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      
      // easeOutExpo
      const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      
      setCount(Math.floor(easeProgress * end));
      
      if (progress < 1) {
        animationFrame = window.requestAnimationFrame(step);
      }
    };
    
    if (end > 0) {
      animationFrame = window.requestAnimationFrame(step);
    } else {
      setCount(0);
    }

    return () => window.cancelAnimationFrame(animationFrame);
  }, [end, duration]);

  return count;
}

export default function StatsCounter() {
  const [stats, setStats] = useState({ unique_visitors: 0, total_attempts: 0, problems_solved: 0 });
  
  useEffect(() => {
    let mounted = true;
    const fetchStats = async () => {
      try {
        const data = await getStats();
        if (mounted) {
          setStats(data);
        }
      } catch (err) {
        console.error("Failed to fetch stats", err);
      }
    };
    fetchStats();
    return () => { mounted = false; };
  }, []);

  const uniqueVisitors = useCountUp(stats.unique_visitors);
  const totalAttempts = useCountUp(stats.total_attempts);
  const problemsSolved = useCountUp(stats.problems_solved);

  return (
    <div style={{ marginTop: 24, display: "flex", gap: 32, flexWrap: "wrap", padding: "16px 20px", backgroundColor: "var(--card)", border: "1px solid var(--border)", borderRadius: "var(--radius)" }}>
      {[
        { val: uniqueVisitors.toLocaleString(), label: "unique visitors" },
        { val: totalAttempts.toLocaleString(), label: "problem attempts" },
        { val: problemsSolved.toLocaleString(), label: "problems solved" },
      ].map(({ val, label }) => (
        <div key={label} style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
          <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: 18, color: "var(--foreground)", letterSpacing: "-0.02em" }}>
            {val}
          </span>
          <span style={{ fontFamily: "var(--font-dm-sans)", fontSize: 13, color: "var(--muted-foreground)" }}>
            {label}
          </span>
        </div>
      ))}
    </div>
  );
}
