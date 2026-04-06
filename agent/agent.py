def decide_action(observation):
    confidence = observation.get("confidence_score", 0)
    severity = observation.get("severity_level", "low").lower()
    reports = observation.get("related_reports", 0)
    verified = observation.get("verified_sources", 0)
    source = observation.get("source", "").lower()

    trusted_sources = ["gov_alert", "official_news", "disaster_agency"]
    weak_sources = ["random_blog", "anonymous_post", "unknown_user"]

    if severity == "high" and (reports >= 3 or source in trusted_sources):
        return "ESCALATE_ALERT"

    if source in weak_sources and confidence < 0.3 and reports == 0:
        return "IGNORE"

    if verified == 0 and confidence >= 0.3:
        return "VERIFY"

    return "REQUEST_MORE_INFO"


if __name__ == "__main__":
    sample_obs = {
        "headline": "Dam overflow warning",
        "source": "gov_alert",
        "confidence_score": 0.9,
        "location": "Chennai",
        "time_since_post": "1 minute",
        "related_reports": 5,
        "verified_sources": 0,
        "severity_level": "high"
    }

    action = decide_action(sample_obs)
    print("Predicted Action:", action)