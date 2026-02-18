from pathlib import Path
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


DB_PATH = Path(__file__).resolve().parents[1] / "support.db"


def get_sql_agent():
    """
    Creates a ReAct-style SQL agent using SQLDatabaseToolkit + create_agent.
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    system_prompt = f"""
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {db.dialect} query to run,
then look at the results of the query and return the answer.

Always:
- Start by listing the tables (sql_db_list_tables)
- Then inspect schemas (sql_db_schema)
- Use sql_db_query_checker before sql_db_query
- Limit results to 5 rows unless user specifies otherwise
- Never modify the database (no INSERT/UPDATE/DELETE)
"""

    agent = create_agent(
        llm,
        tools,
        system_prompt=system_prompt,
    )

    return agent, tools


def run_sql_agent(query: str) -> str:
    """
    Executes a natural-language query using the SQL agent.
    Returns the final LLM answer.
    """

    agent, _ = get_sql_agent()

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    # ReAct agents return a dict with "messages"
    final_msg = result["messages"][-1].content
    return final_msg