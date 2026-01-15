from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from model import predict_winner
from enum import Enum

app = FastAPI(title="The Architect's Sports Oracle", version="2.0")

# Tell Python where to find your dashboard file
app.mount("/static", StaticFiles(directory="static"), name="static")

class Sport(str, Enum):
    NFL = "NFL"
    NBA = "NBA"
    NCAAB = "NCAAB"
    MLB = "MLB"
    NHL = "NHL"

class MatchRequest(BaseModel):
    sport: Sport
    home_team: str
    away_team: str

# This makes the dashboard the FIRST thing people see
@app.get("/")
def read_root():
    return FileResponse('static/index.html')

@app.post("/predict")
def get_prediction(match: MatchRequest):
    result = predict_winner(match.home_team, match.away_team, match.sport)
    return result