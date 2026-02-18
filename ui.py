import streamlit as st
import asyncio
from fastmcp import Client

MCP_URL = "http://127.0.0.1:8000/mcp"


async def call_mcp(full_history: str) -> str:
    """
    Calls the MCP workflow tool using the tutorial-style FastMCP Client.
    Sends the entire chat history as context.
    """
    client = Client(MCP_URL)

    async with client:
        result = await client.call_tool(
            name="workflow",
            arguments={"query": full_history},
        )
        return result


def format_history_for_mcp(messages):
    """
    Convert session messages into a single text block for the MCP tool.
    """
    lines = []
    for role, content in messages:
        prefix = "User:" if role == "user" else "Assistant:"
        lines.append(f"{prefix} {content}")
    return "\n".join(lines)


def main():
    st.set_page_config(page_title="Support Assistant Chat", layout="wide")
    st.title("💬 Support Assistant (Sessional MCP Chat)")

    # ---------------------------------------------------------
    # Initialize session state
    # ---------------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []  # list of (role, content)

    # ---------------------------------------------------------
    # Sidebar: Clear session
    # ---------------------------------------------------------
    with st.sidebar:
        st.header("Session")
        if st.button("🧹 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # ---------------------------------------------------------
    # Render chat history
    # ---------------------------------------------------------
    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.write(content)

    # ---------------------------------------------------------
    # User input
    # ---------------------------------------------------------
    user_input = st.chat_input("Ask something…")

    if user_input:
        # Add user message
        st.session_state.messages.append(("user", user_input))

        with st.chat_message("user"):
            st.write(user_input)

        # Prepare full history for MCP
        full_history = format_history_for_mcp(st.session_state.messages)

        # Assistant response placeholder
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.write("Thinking…")

            # Call MCP server with full history
            result = asyncio.run(call_mcp(full_history))
            placeholder.write(result.structured_content['result'])

        # Save assistant message
        st.session_state.messages.append(("assistant", result.structured_content['result']))


if __name__ == "__main__":
    main()