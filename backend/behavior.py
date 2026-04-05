import sqlite3
import os
import random

def calculate_behavior_risk(user_id=1, current_typing=65, current_mouse=220, current_clicks=40, db_path=None):
    if db_path is None:
        db_path = os.path.join("db", "history.db")
        
    # Fetch baseline
    from database.db import get_user_baseline
    row = get_user_baseline(user_id)
    
    if not row:
        # Default baseline if not in DB
        baseline_typing, baseline_mouse, baseline_clicks = 65, 220, 40
    else:
        baseline_typing, baseline_mouse, baseline_clicks = row
    
    # Calculate absolute differences
    typing_diff = abs(current_typing - baseline_typing)
    mouse_diff = abs(current_mouse - baseline_mouse)
    click_diff = abs(current_clicks - baseline_clicks)
    
    # Total Score as per requirement
    total_score = typing_diff + mouse_diff + click_diff
    
    if total_score <= 30:
        risk_level = "Normal"
        normalized_score = total_score / 100.0 # Just for integration internal scoring
    elif total_score <= 60:
        risk_level = "Medium Risk"
        normalized_score = 0.4 + (total_score / 100.0)
    else:
        risk_level = "High Risk"
        normalized_score = 0.8 + (total_score / 100.0)
        
    return total_score, min(normalized_score, 1.0), risk_level

def simulate_file_behavior():
    # Behavioral Engine sequence for API calls
    API_MAP = {
        "CreateFile": "FR",
        "WriteFile": "FW",
        "RegSetValue": "RE",
        "InternetOpen": "NC",
        "CreateProcess": "PS"
    }
    apis = list(API_MAP.keys())
    sequence_apis = [random.choice(apis) for _ in range(10)]
    dna = [API_MAP[api] for api in sequence_apis]
    
    suspicious_patterns = [["FW","NC"], ["NC","RE"], ["PS","FW"], ["FR", "FW", "NC"]]
    detected = []
    
    # Check 2-grams
    for i in range(len(dna)-1):
        pair = [dna[i], dna[i+1]]
        if pair in suspicious_patterns:
            detected.append(" → ".join(pair))
            
    # Check 3-grams
    for i in range(len(dna)-2):
        trio = [dna[i], dna[i+1], dna[i+2]]
        if trio in suspicious_patterns:
            detected.append(" → ".join(trio))
            
    return sequence_apis, dna, list(set(detected))
