def grade(predicted, correct, time_taken, severity):
    score = 0
    
    if predicted == correct:
        score += 1
        
        if correct == "ESCALATE_ALERT" and time_taken <= 2:
            score += 0.5
    
    elif predicted in ["VERIFY", "REQUEST_MORE_INFO"]:
        score += 0.3
    
    if predicted == "IGNORE" and severity == "high":
        score -= 2
    
    return score
