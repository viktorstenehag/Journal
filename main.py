from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
import sqlite3

app = FastAPI(title="AI-Analyst")

conn = sqlite3.connect("logs.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               timestamp TEXT NOT NULL,
               content TEXT
               )
""")
conn.commit()
conn.close()

class DailyLog(BaseModel):
    timestamp: Optional[date] = date.today()
    content: Optional[str] = None

@app.post("/log/")
def create_log(log: DailyLog):
    try:
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs(timestamp, content)
            VALUES (?, ?)
        """, (log.timestamp.isoformat(), log.content))
        conn.commit()
        conn.close()
        return {"message": "Log saved succesfully", "Data": log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/logs/")
def get_logs():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return {"logs": rows}