def test_sql_agent_toolkit_real_call():
    """
    Real OpenAI test:
    - Loads SQL agent using SQLDatabaseToolkit + create_agent
    - Prints available tools (sanity check)
    - Executes a cheap real OpenAI call
    """

    import os
    from app.agents.sql_agent import get_sql_agent, run_sql_agent

    # Ensure API key is present
    assert "OPENAI_API_KEY" in os.environ, "OPENAI_API_KEY must be set."

    # Build agent + tools
    agent, tools = get_sql_agent()

    print("\n--- SQL Toolkit Tools ---")
    for tool in tools:
        print(f"{tool.name}: {tool.description}\n")

    # Cheap real query
    query = "Summarize customer Ema's profile."

    result = run_sql_agent(query)

    assert isinstance(result, str)
    assert len(result.strip()) > 0
    assert "Ema" in result or "customer" in result