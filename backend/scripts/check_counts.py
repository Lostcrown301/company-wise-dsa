import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

with engine.connect() as conn:
    v_count = conn.execute(text("SELECT COUNT(*) FROM visitors")).scalar()
    a_count = conn.execute(text("SELECT COUNT(*) FROM attempts")).scalar()
    s_count = conn.execute(text("SELECT COUNT(*) FROM solves")).scalar()
    print(f"Visitors: {v_count}, Attempts: {a_count}, Solves: {s_count}")
    
    # If 0, insert a dummy visitor for testing
    if v_count == 0:
        print("Inserting a dummy visitor...")
        conn.execute(text("INSERT INTO visitors (id) VALUES ('00000000-0000-0000-0000-000000000001'::uuid)"))
        conn.execute(text("INSERT INTO attempts (id, visitor_id, problem_slug) VALUES ('00000000-0000-0000-0000-000000000002'::uuid, '00000000-0000-0000-0000-000000000001'::uuid, 'two-sum')"))
        conn.execute(text("INSERT INTO solves (id, visitor_id, problem_slug) VALUES ('00000000-0000-0000-0000-000000000003'::uuid, '00000000-0000-0000-0000-000000000001'::uuid, 'two-sum')"))
        conn.commit()
        
        v_count = conn.execute(text("SELECT COUNT(*) FROM visitors")).scalar()
        a_count = conn.execute(text("SELECT COUNT(*) FROM attempts")).scalar()
        s_count = conn.execute(text("SELECT COUNT(*) FROM solves")).scalar()
        print(f"After Insert -> Visitors: {v_count}, Attempts: {a_count}, Solves: {s_count}")
