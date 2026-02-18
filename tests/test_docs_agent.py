def test_docs_agent_real_call():
    """
    Minimal real test:
    - Uses the real docs agent
    - Retrieves from the real vectorstore
    - Confirms the LLM returns a non-empty summary
    """

    from app.agents.docs_agent import run_docs_agent

    # Keep the query extremely cheap
    query = "Explain the overtime policy."

    result = run_docs_agent(query)

    assert isinstance(result, str)
    assert len(result.strip()) > 0
    assert "overtime" in result.lower() or "policy" in result.lower()