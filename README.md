# Leaderbolt Operational Review System

A multi-agent AI pipeline that researches any public tech company and generates
a structured operational review — automatically.

Built as part of the Leaderbolt AI Agent Development internship assignment.

---

## How It Works
User Input → Company Resolver → Wikipedia Scraper → Agent A → Agent B → Final Report


**Agent A — Business Research Analyst**
Scrapes the Wikipedia page of the given company and produces a clean,
factual 150-word summary covering founding, products, business model, and strategy.

**Agent B — Operations Strategy Consultant**
Reads Agent A's summary and generates a structured 3-bullet operational review
covering strengths, challenges, and strategic opportunities.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| LangGraph | Multi-agent pipeline orchestration |
| LangChain + Groq | LLM integration (LLaMA 3.3 70B) |
| Wikipedia API | Public data source |
| Python Dotenv | Secure API key management |

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Taha-Mohii/leaderbolt-ai-crew.git
cd leaderbolt-ai-crew
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create a `.env` file**
GROQ_API_KEY=your_groq_api_key_here

**4. Run**
```bash
python main.py
```

---

## Example Output
Enter company: google
ℹ️  Resolved 'google' → 'Google'
[Scraping 'Google'...]
[Done. Running agents...]
==================================================
REPORT — GOOGLE
[Agent A — Research Summary]
Google LLC was founded in 1998 by Larry Page and Sergey Brin...
[Agent B — Operational Review]

Strength: Google's diversified product portfolio provides robust cross-platform
revenue streams and strong market positioning.
Challenge: Heavy reliance on advertising revenue makes Google vulnerable to
market fluctuations and increasing regulatory scrutiny.
Opportunity: Strategic investments in AI and cloud computing position Google
to expand into high-growth enterprise and developer markets.

==================================================

---

## Features

- Accepts any company name — common variations resolved automatically
  (e.g. `apple` → `Apple Inc.`, `meta` → `Meta Platforms`)
- Handles Wikipedia page variants gracefully
- Clean sequential agent handoff via LangGraph StateGraph
- Fully local — no paid APIs beyond Groq (free tier sufficient)

---

## Author

**Taha Mohi Ud Din Rather**
B.Tech CSE — College of Engineering Trivandrum
[github.com/Taha-Mohii](https://github.com/Taha-Mohii)






