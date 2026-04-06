def grade(predicted, correct, time_taken):
    if predicted == correct:
        if correct == "ESCALATE_ALERT" and time_taken <= 2:
            return 1.0
        return 1.0
    
    elif predicted in ["VERIFY", "REQUEST_MORE_INFO"]:
        return 0.5
    
    else:
        return 0.0
