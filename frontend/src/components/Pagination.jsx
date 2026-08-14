import React from "react";

export default function Pagination({ page, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  const pages = [];
  
  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    if (page <= 4) {
      pages.push(1, 2, 3, 4, 5, '...', totalPages);
    } else if (page >= totalPages - 3) {
      pages.push(1, '...', totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
    } else {
      pages.push(1, '...', page - 1, page, page + 1, '...', totalPages);
    }
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px', flexWrap: 'wrap', marginTop: '32px' }}>
      <button 
        onClick={() => onPageChange(page - 1)} 
        disabled={page === 1}
        style={{ fontFamily: 'var(--font-dm-sans)', fontSize: 13, padding: '6px 12px', cursor: page === 1 ? 'default' : 'pointer', opacity: page === 1 ? 0.5 : 1, background: 'none', border: '1px solid var(--border)', borderRadius: 'var(--radius)', color: 'var(--foreground)' }}
      >
        Previous
      </button>
      
      {pages.map((p, i) => (
        <button
          key={i}
          disabled={p === '...'}
          onClick={() => p !== '...' && onPageChange(p)}
          style={{ fontFamily: 'var(--font-dm-mono)', fontSize: 13, padding: '6px 12px', cursor: p === '...' ? 'default' : 'pointer', background: p === page ? 'var(--accent)' : 'none', border: p === '...' ? 'none' : '1px solid var(--border)', borderRadius: 'var(--radius)', color: p === page ? 'var(--primary-foreground)' : 'var(--foreground)', minWidth: 36 }}
        >
          {p}
        </button>
      ))}

      <button 
        onClick={() => onPageChange(page + 1)} 
        disabled={page === totalPages}
        style={{ fontFamily: 'var(--font-dm-sans)', fontSize: 13, padding: '6px 12px', cursor: page === totalPages ? 'default' : 'pointer', opacity: page === totalPages ? 0.5 : 1, background: 'none', border: '1px solid var(--border)', borderRadius: 'var(--radius)', color: 'var(--foreground)' }}
      >
        Next
      </button>
    </div>
  );
}
