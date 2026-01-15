from fastapi import FastAPI, HTTPException
from model import predict_matchup # <--- IMPORTING THE CHEF

app = FastAPI(
    title="The Architect's Sports Oracle",
    description="Neural-Network style prediction engine for NFL games.",
    version="2.0"
)

@app.get("/")
def home():
    return {"message": "System Online. Use /predict?home=Bills&away=Chiefs"}

# The New Dynamic Endpoint
@app.get("/predict")
def get_prediction(home: str, away: str):
    """
    Query Example: /predict?home=Bills&away=Dolphins
    """
    result = predict_matchup(home, away)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return {
        "architect_analysis": result,
        "disclaimer": "Algorithm is for entertainment purposes."
    }