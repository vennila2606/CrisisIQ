def grade(action, correct_action, severity, time_step, verified_sources):
    """
    Returns a score strictly between 0.001 and 0.999.
    Each condition is mutually exclusive - no double counting.
    """

    # ── Base score from action correctness (pick exactly one branch) ──
    if action == correct_action:
        if action == "ESCALATE_ALERT" and time_step <= 2:
            score = 0.95   # fast correct escalation
        else:
            score = 0.85   # correct but not fast

    elif action == "VERIFY":
        score = 0.55       # partial credit - safe choice

    elif action == "REQUEST_MORE_INFO":
        score = 0.45       # partial credit - cautious

    elif action == "IGNORE" and severity == "high":
        score = 0.05       # very dangerous mistake

    else:
        score = 0.15       # wrong but not catastrophic

    # ── Single time penalty (only if slow AND not already penalised) ──
    if time_step > 3 and score > 0.5:
        score = score - 0.10

    # ── Single verified-sources bonus (only if not already high) ──
    if verified_sources >= 2 and score < 0.90:
        score = score + 0.05

    # ── Hard clamp — guaranteed strictly within (0.001, 0.999) ──
    score = max(0.001, min(0.999, round(score, 3)))

    return score