import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = 'neondb'"))
    conn.commit()
print("Terminated stale connections")
