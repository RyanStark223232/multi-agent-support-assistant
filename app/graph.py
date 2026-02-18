from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from app.agents.sql_agent import run_sql_agent
from app.agents.docs_agent import run_docs_agent
from langchain_openai import ChatOpenAI


# -----------------------------
# 1. Define the graph state
# -----------------------------
class AgentState(TypedDict):
    query: str
    route: Optional[str]
    answer: Optional[str]


# -----------------------------
# 2. Router agent
# -----------------------------
def router_node(state: AgentState) -> AgentState:
    """
    Uses an LLM to decide whether the query should go to:
    - SQL agent
    - Docs agent
    """

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
You are a routing classifier.

Decide whether the user's query should be answered using:
- "SQL" → if the question is about customers, tickets, IDs, dates, counts, or anything in the database.
- "DOCS" → if the question is about policies, handbook content, rules, procedures, or HR topics.

Return ONLY one word: SQL or DOCS.

User query:
{state["query"]}
"""

    result = llm.invoke(prompt).content.strip().upper()

    if result not in ("SQL", "DOCS"):
        result = "DOCS"  # safe fallback

    return {**state, "route": result}


# -----------------------------
# 3. SQL agent node
# -----------------------------
def sql_node(state: AgentState) -> AgentState:
    answer = run_sql_agent(state["query"])
    return {**state, "answer": answer}


# -----------------------------
# 4. Docs agent node
# -----------------------------
def docs_node(state: AgentState) -> AgentState:
    answer = run_docs_agent(state["query"])
    return {**state, "answer": answer}


# -----------------------------
# 5. Build the graph
# -----------------------------
def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("sql_agent", sql_node)
    graph.add_node("docs_agent", docs_node)

    # Entry point
    graph.set_entry_point("router")

    # Conditional routing
    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "SQL": "sql_agent",
            "DOCS": "docs_agent",
        },
    )

    # Both agent nodes end the workflow
    graph.add_edge("sql_agent", END)
    graph.add_edge("docs_agent", END)

    return graph.compile()


# -----------------------------
# 6. Convenience function
# -----------------------------
def run_workflow(query: str) -> str:
    workflow = build_graph()
    result = workflow.invoke({"query": query})
    return result["answer"]

if __name__ == "__main__":
    print(run_workflow("Explain the overtime policy."))
    print(run_workflow("Summarize customer Ema's profile."))
