---
license: mit
title: CrisiIQ
sdk: docker
emoji: 👀
colorFrom: pink
colorTo: purple
short_description: An RL environment where AI agents verify crisis reports
---
🛰️ CrisisIQ: Crisis Intelligence & News Verification Environment
📌 Overview
CrisisIQ is an AI simulation environment designed to evaluate how intelligent agents make decisions during crisis situations involving uncertain and potentially misleading information.

The system models real-world scenarios such as disaster alerts, social media reports, and emergency warnings, where agents must decide how to respond under time pressure, uncertainty, and risk.

🚨 Motivation
During real-world crises (floods, earthquakes, conflicts):

Misinformation spreads rapidly False alerts create panic Delayed decisions can cost lives

Traditional systems focus only on classification (true/false), but real-world decision-making requires balancing:

Speed vs accuracy Risk vs uncertainty Incomplete information

CrisisIQ simulates this challenge and evaluates how well AI agents handle it.

🌍 Environment Description
CrisisIQ is a step-based simulation environment where:

The agent receives a crisis-related observation The agent selects an action The environment evaluates the decision A reward is assigned based on correctness and timing

The environment includes:

dynamic state updates multi-step reasoning partial observability 👀 Observation Space

Each observation represents a real-world information signal.

Structure: { "headline": "Bridge collapse reported", "source": "twitter", "confidence_score": 0.45, "location": "Chennai", "time_since_post": "5 minutes", "related_reports": 2, "verified_sources": 0, "severity_level": "high" } Features: Feature Description headline Text describing event source Origin of information confidence_score Reliability estimate related_reports Supporting reports count severity_level Risk level (low/medium/high) time_since_post Recency of information verified_sources Number of confirmations

🎯 Action Space
The agent can choose one of the following actions:

Action Description VERIFY Check credibility of information ESCALATE_ALERT Trigger emergency response IGNORE Dismiss false or irrelevant info REQUEST_MORE_INFO Ask for additional data

🧩 Task Design & Difficulty
The environment includes multiple tasks categorized by difficulty:

🟢 Easy Tasks Clearly fake or low-risk information Low confidence, no supporting reports

Expected Action: IGNORE

🟡 Medium Tasks Uncertain reports with partial evidence Moderate confidence and some reports

Expected Action: VERIFY or REQUEST_MORE_INFO

🔴 Hard Tasks High-risk, time-sensitive crises Multiple reports, high severity

Expected Action: ESCALATE_ALERT

⚠️ Adversarial / Tricky Cases Fake but viral information Conflicting signals High severity but low confidence

These require deeper reasoning and careful decision-making.

🧠 Reward System
The agent is evaluated using a reward function:

Scenario Reward Correct decision +1 Early escalation +1.5 Verification step +0.5 Request info +0.3 False alarm -1 Ignoring real crisis -2

This encourages:

correct decisions timely actions cautious reasoning ⚙️ Project Structure CrisisIQ/ │ ├── data/ │ ├── tasks.json │ └── dataset_generator.py │ ├── env/ │ └── environment.py │ ├── agent/ │ └── agent.py │ ├── evaluation/ │ ├── evaluator.py │ └── grader.py │ ├── scripts/ │ ├── run.py │ └── baseline_inference.py │ └── README.md ▶️ Setup & Installation

Clone repository git clone cd CrisisIQ
Install dependencies pip install -r requirements.txt
🚀 Usage
Run evaluation (FULL SYSTEM) python evaluation/evaluator.py Run single simulation python scripts/run.py Generate dataset python data/dataset_generator.py Run LLM baseline (optional) python scripts/baseline_inference.py

📊 Baseline Performance
Example results from evaluation:

Metric Value Total Score 10 – 15 Accuracy 0.6 – 0.8 Interpretation: Higher score → better decision-making Accuracy reflects correct final actions Variation expected due to task randomness 🤖 Agents Implemented

Rule-Based Agent Uses predefined logic Fast and consistent Limited adaptability
LLM-Based Agent (Optional) Uses language model reasoning Handles complex ambiguity More flexible but slower
🧠 Key Innovation
Unlike traditional classification systems, CrisisIQ focuses on:

Decision-making under uncertainty, not just prediction.

The agent must:

act quickly ⚡ avoid mistakes 🎯 handle incomplete information 📉

🚀 Future Work
Reinforcement learning agents Multi-agent coordination Real-time data integration Trust scoring for sources Time-decay reliability modeling

🎤 Conclusion
CrisisIQ demonstrates how AI can assist in crisis management by making reliable and timely decisions under uncertainty.

This project highlights the importance of balancing speed, accuracy, and risk in real-world intelligent systems.

📜 License
This project is for academic and research purposes.