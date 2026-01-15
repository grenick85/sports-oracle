import random

# A simple "Power Ranking" database based on typical season stats.
# In a real Neural Network, these would be dynamic weights trained on 10 years of data.
team_stats = {
    "Bills": {"offense": 92, "defense": 88, "home_field": 4},
    "Chiefs": {"offense": 94, "defense": 85, "home_field": 5},
    "Dolphins": {"offense": 89, "defense": 78, "home_field": 3},
    "Raiders": {"offense": 76, "defense": 72, "home_field": 3},
    "Eagles": {"offense": 88, "defense": 84, "home_field": 4},
    "Cowboys": {"offense": 85, "defense": 82, "home_field": 4},
    "Ravens": {"offense": 90, "defense": 91, "home_field": 4},
    "Steelers": {"offense": 78, "defense": 88, "home_field": 5},
}

def predict_matchup(home_team: str, away_team: str):
    """
    Calculates the winner based on offense, defense, and home field advantage.
    Mimics a Feed-Forward Neural Network logic.
    """
    
    # 1. Validation (Check if teams exist in our database)
    if home_team not in team_stats or away_team not in team_stats:
        return {"error": "Team not found in database."}

    home = team_stats[home_team]
    away = team_stats[away_team]

    # 2. The Algorithm (The "Secret Sauce")
    # We calculate a 'Power Score' for this specific game.
    home_score = (home["offense"] * 0.6) + (home["defense"] * 0.4) + home["home_field"]
    away_score = (away["offense"] * 0.6) + (away["defense"] * 0.4)
    
    # Add a "Chaos Factor" (Any Given Sunday randomness)
    # This makes the model realistic—it won't return the EXACT same decimal every time.
    chaos = random.uniform(-2, 2) 
    final_margin = (home_score - away_score) + chaos

    # 3. Determine Winner
    if final_margin > 0:
        winner = home_team
        confidence = min(50 + (final_margin * 1.5), 99) # Cap at 99%
    else:
        winner = away_team
        confidence = min(50 + (abs(final_margin) * 1.5), 99)

    return {
        "matchup": f"{away_team} @ {home_team}",
        "predicted_winner": winner,
        "confidence_score": f"{confidence:.1f}%",
        "logic": "Offensive Efficiency weighted vs Defensive Solidity"
    }