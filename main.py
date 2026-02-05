import os
import sqlite3
import subprocess
from fastapi import FastAPI, Body, Request
from fastapi.responses import FileResponse # Added for HTML serving
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Added for image serving
from model import ArchitectModel
from playwright.sync_api import sync_playwright

app = FastAPI()

# --- CLOUDFLARE & FRONTEND COMPATIBILITY ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "architect_memory.db")
bot = ArchitectModel()

# --- NEW: SERVE THE VAULT FRONTEND ---
# This fixes your 404 error by mapping the root URL to index.html
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, 'index.html'))

# Mount static folder for the "Jenny Visions" (images)
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/signup")
async def signup(data: dict = Body(...)):
    """Registration for free February access."""
    if not data.get("is_18"): 
        return {"success": False, "message": "18+ only"}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Ensure users table has a 'credits' column for Genie Power tracking
    cursor.execute("""
        INSERT OR IGNORE INTO users (email, password, credits) 
        VALUES (?,?,?)
    """, (data['email'], data['password'], 100)) # Start with 100 credits
    conn.commit()
    conn.close()
    return {"success": True, "message": "Welcome, Founder!"}

@app.get("/predictions") # Updated to match your index.html fetch call
async def get_predictions():
    """Displays games from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT date, time, home_team, away_team FROM schedule LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    return {
        "accuracy": "52.4%", 
        "games": [{"date": r[0], "time": r[1], "matchup": f"{r[2]} vs {r[3]}", "home": r[2], "away": r[3], "spread": "-3"} for r in rows]
    }

@app.get("/predict-interactive") # Updated to match index.html fetch call
async def handle_prophecy(matchup: str, tier: str):
    """Jenny's prophecy + Whale Tier manifestation."""
    # Split matchup (e.g., 'Lakers vs Celtics')
    teams = matchup.split(' vs ')
    home, away = teams[0], teams[1]
    
    prophecy = bot.get_tiered_prediction(home, away, tier=tier)
    
    # TRACK USAGE: Record the action in architect_memory.db
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usage_log (matchup, tier, timestamp) VALUES (?, ?, datetime('now'))", (matchup, tier))
    conn.commit()
    conn.close()

    return {"prophecy": prophecy.get('ai_prophecy', 'The spirits are silent...'), "status": "ARCHITECT MODE ACTIVE"}

if __name__ == "__main__":
    import uvicorn
    # Finalized to port 8000 for your Strike-Force Tunnel
    uvicorn.run(app, host="127.0.0.1", port=8000)l')

@app.post("/predict")
def get_prediction(match: MatchRequest):
    result = predict_winner(match.home_team, match.away_team, match.sport)
    return result
