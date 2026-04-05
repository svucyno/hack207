def get_prediction(model, features, behavior_score, urls_detected=False):
    static_proba = float(model.predict_proba(features)[0][1])
    
    # Fused calculation final_score = file_score + behavior_score
    # In this logic static_proba represents the file score (normalized)
    final_score = (static_proba * 0.6) + (behavior_score * 0.4)
    
    # Explicit URL rule override
    if urls_detected:
        final_score = min(final_score + 0.3, 1.0)
        
    is_malicious = final_score > 0.5
    return is_malicious, final_score, static_proba
