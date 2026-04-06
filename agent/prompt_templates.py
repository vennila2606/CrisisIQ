def build_crisis_prompt(observation):
    return f"""
You are a crisis intelligence agent.

Given the following report:
Headline: {observation.get('headline')}
Source: {observation.get('source')}
Confidence Score: {observation.get('confidence_score')}
Location: {observation.get('location')}
Time Since Post: {observation.get('time_since_post')}
Related Reports: {observation.get('related_reports')}
Verified Sources: {observation.get('verified_sources')}
Severity Level: {observation.get('severity_level')}

Choose exactly one action:
VERIFY
ESCALATE_ALERT
IGNORE
REQUEST_MORE_INFO
"""