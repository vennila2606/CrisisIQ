def grade(action, correct_action, severity, time_step, verified_sources):
    """
    Must return strictly between 0 and 1 (never 0.0 or 1.0)
    """
    if action == correct_action:
        if time_step == 1:
            score = 0.95  # fast and correct
        elif verified_sources > 0:
            score = 0.85  # correct with verification
        else:
            score = 0.75  # correct

    elif action == "VERIFY":
        score = 0.55  # safe but not final answer

    elif action == "REQUEST_MORE_INFO":
        score = 0.45  # cautious

    elif action == "IGNORE" and severity == "high":
        score = 0.05  # dangerous

    elif action == "ESCALATE_ALERT" and severity == "low":
        score = 0.15  # overreaction

    else:
        score = 0.25  # wrong

    # ✅ Guarantee strictly between 0 and 1
    return max(0.01, min(0.99, score))