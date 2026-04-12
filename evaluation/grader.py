def _compute_score(action, correct_action, severity, time_step, verified_sources):
    """Core scoring logic - mutually exclusive branches, no double counting."""

    if action == correct_action:
        if action == "ESCALATE_ALERT" and time_step <= 2:
            score = 0.95
        else:
            score = 0.85
    elif action == "VERIFY":
        score = 0.55
    elif action == "REQUEST_MORE_INFO":
        score = 0.45
    elif action == "IGNORE" and severity == "high":
        score = 0.05
    else:
        score = 0.15

    # Single time penalty
    if time_step > 3 and score > 0.5:
        score = score - 0.10

    # Single verified-sources bonus
    if verified_sources >= 2 and score < 0.90:
        score = score + 0.05

    # Hard clamp
    return max(0.001, min(0.999, round(score, 3)))


def grade(action, correct_action, severity, time_step, verified_sources):
    return _compute_score(action, correct_action, severity, time_step, verified_sources)


class EasyGrader:
    """Grader for Task 1 - Fake News Detection (easy)."""
    def grade(self, action, correct_action="IGNORE", severity="low",
              time_step=1, verified_sources=0):
        return _compute_score(action, correct_action, severity, time_step, verified_sources)


class MediumGrader:
    """Grader for Task 2 - Uncertain Crisis Report (medium)."""
    def grade(self, action, correct_action="VERIFY", severity="medium",
              time_step=1, verified_sources=1):
        return _compute_score(action, correct_action, severity, time_step, verified_sources)


class HardGrader:
    """Grader for Task 3 - High-Risk Dam Overflow (hard)."""
    def grade(self, action, correct_action="ESCALATE_ALERT", severity="high",
              time_step=1, verified_sources=4):
        return _compute_score(action, correct_action, severity, time_step, verified_sources)