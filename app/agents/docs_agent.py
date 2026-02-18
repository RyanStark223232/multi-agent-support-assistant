from langchain_openai import ChatOpenAI
from app.vectorstore import get_vectorstore


def get_docs_agent():
    """
    Creates a docs agent that:
    - Retrieves relevant chunks from the vectorstore
    - Summarizes them using ChatGPT
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 4})

    return llm, retriever


def run_docs_agent(query: str) -> str:
    """
    Retrieves relevant policy text and summarizes it.
    """

    llm, retriever = get_docs_agent()

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant policy information found."

    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
You are a policy assistant. Summarize the relevant policy information
based strictly on the context below. Be concise and accurate.

User question:
{query}

Relevant policy excerpts:
{context}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content