def grade(action, correct_action, severity, time_step, verified_sources):
    reward = 0

    # ✅ Correct decision
    if action == correct_action:
        reward += 1

        # Bonus for fast escalation
        if action == "ESCALATE_ALERT" and time_step <= 2:
            reward += 1.5

    # 🟡 Partial correct decisions
    elif action == "VERIFY":
        reward += 0.5

    elif action == "REQUEST_MORE_INFO":
        reward += 0.3

    # ❌ Wrong decisions
    elif action == "IGNORE" and severity == "high":
        reward -= 2   # very bad

    else:
        reward -= 1   # normal wrong

    # ⏱ Time penalty (slow decision)
    if time_step > 3:
        reward -= 0.2

    # 📊 Bonus for gathering info
    if verified_sources >= 2:
        reward += 0.2

    return reward