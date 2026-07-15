import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict
import wikipediaapi

load_dotenv()

# Maps common names to extract wikipedia titles.
TECH_COMPANY_MAP = {
    "apple": "Apple Inc.", "microsoft": "Microsoft", "google": "Google",
    "amazon": "Amazon (company)", "meta": "Meta Platforms", "facebook": "Meta Platforms",
    "netflix": "Netflix", "tesla": "Tesla, Inc.", "nvidia": "Nvidia",
    "intel": "Intel", "amd": "AMD", "ibm": "IBM", "oracle": "Oracle Corporation",
    "salesforce": "Salesforce", "adobe": "Adobe Inc.", "uber": "Uber",
    "airbnb": "Airbnb", "spotify": "Spotify", "twitter": "Twitter",
    "snap": "Snap Inc.", "tiktok": "TikTok", "alibaba": "Alibaba Group",
    "samsung": "Samsung", "sony": "Sony"
}

def resolve_company(name: str) -> str:
    key = name.strip().lower()
    if key in TECH_COMPANY_MAP:
        print(f"  ℹ️  Resolved '{name}' → '{TECH_COMPANY_MAP[key]}'")
        return TECH_COMPANY_MAP[key]
    return name

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not found.")
        sys.exit(1)
    return ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key, temperature=0.3)

llm = get_llm()

# Data passing between agents.
class AgentState(TypedDict):
    company: str
    wiki_content: str
    summary: str
    review: str

def scrape_wikipedia(name: str) -> str | None:
    wiki = wikipediaapi.Wikipedia(language='en', user_agent='LeaderboltAssignment/1.0')
    for variant in [name, name.title(), f"{name} (company)"]:
        page = wiki.page(variant)
        if page.exists():
            return page.text[:3000]
    return None

# Agent A reads wikipedia and writes summary.
def agent_researcher(state: AgentState) -> AgentState:
    prompt = f"""Summarize this Wikipedia content about {state['company']} in 150 words.
Cover: founding, products, business model, recent strategy. Plain paragraph only.

{state['wiki_content']}"""
    state['summary'] = llm.invoke([HumanMessage(content=prompt)]).content
    return state


#  Agent B reads summary and writes 3 bullet points based on that.
def agent_reviewer(state: AgentState) -> AgentState:
    prompt = f"""You are an Operations Strategy Consultant. Write exactly 3 bullets for {state['company']}.
NO intro. NO conclusion. ONLY the 3 bullets below.

Each bullet must be ONE sentence, 12-18 words, focused on OPERATIONS:
- Supply chain, workforce management, infrastructure scaling, R&D efficiency, global distribution

Format:
• Strength: [operational strength, 12-18 words]
• Challenge: [operational challenge, 12-18 words]
• Opportunity: [operational opportunity, 12-18 words]

Research:
{state['summary']}"""
    
    review = llm.invoke([HumanMessage(content=prompt)]).content
    
    # Normalizing bullet points to consistent format.
    for label in ["Strength", "Challenge", "Opportunity"]:
        review = review.replace(f"- [{label}]:", f"• [{label}]:")
        review = review.replace(f"- {label}:", f"• {label}:")
        review = review.replace(f"• [{label}]:", f"• {label}:")
    
    state['review'] = review
    return state

#  Build sequential workflow between  A and B.
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("researcher", agent_researcher)
    graph.add_node("reviewer", agent_reviewer)
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "reviewer")
    graph.add_edge("reviewer", END)
    return graph.compile()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  LEADERBOLT OPERATIONAL REVIEW SYSTEM")
    print("="*50)

    company = resolve_company(input("\nEnter company: ").strip())
    if not company:
        print("No company entered.")
        sys.exit(1)

    print(f"\n[Scraping '{company}'...]")
    wiki = scrape_wikipedia(company)
    if not wiki:
        print(f"ERROR: Wikipedia page not found for '{company}'.")
        sys.exit(1)

    result = build_graph().invoke({
        "company": company, "wiki_content": wiki, "summary": "", "review": ""
    })

    print("\n" + "="*50)
    print(f"  REPORT — {company.upper()}")
    print("="*50)
    print("\n[Agent A — Research Summary]")
    print(result['summary'])
    print("\n[Agent B — Operational Review]")
    print(result['review'])
    print("\n" + "="*50)