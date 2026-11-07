import os
import psycopg2

def db_agent(user_name: str = "Hyarel"):
    try:
        conn = psycopg2.connect(host="localhost", dbname="loandb", user="loanuser", password="loan123")
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close(); conn.close()
        return {"source": "postgresql", "user_name": user_name, "cibil_score": 680, "has_one_year_statement": True}
    except Exception as e:
        print("DB fallback used:", e)
        return {"source": "fallback_sample_data", "user_name": user_name, "cibil_score": 680, "has_one_year_statement": True}
