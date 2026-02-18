# Support Assistant — MCP + LangGraph + Streamlit UI

A lightweight multi‑agent support assistant powered by:

- **FastMCP** (HTTP MCP server)
- **LangGraph** workflow routing
- **SQL + Docs agents**
- **Streamlit** chat UI

![](https://github.com/RyanStark223232/multi-agent-support-assistant/blob/master/demo.gif)

## Requirements

- **Python 3.11**
- **pip** or **uv** (recommended)
- **OpenAI API key**

---

## Environment Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

---

### 2. Create a virtual environment (Python 3.11)

#### **Windows (PowerShell)**

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Set Your OpenAI API Key

The agents rely on OpenAI embeddings, so you must set:

### **Windows (PowerShell)**

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

---

## Running the System

Create the SQL database and vector store by running

```bash
python -m app.db.init_db
```

```bash
python -m app.vectorstore
```

You’ll run two terminals:  
one for the MCP server, one for the Streamlit UI.

---

### **Terminal 1 — Start the MCP Server**

```bash
python -m app.mcp_server
```

This starts the FastMCP server at:

```
http://127.0.0.1:8000/mcp
```

---

### **Terminal 2 — Start the Streamlit UI**

```bash
streamlit run streamlit_app.py
```

Then open:

```
http://localhost:8501
```

You now have a fully sessional chat UI that sends the entire conversation history to your MCP workflow tool.

---

## Optional: Test the MCP Server

Run the test suite:

```bash
pytest -q
```

---

## Project Structure

```
app/
  agents/
    sql_agent.py
    docs_agent.py
  db/
    init_db.py
    schema.sql
  graph.py
  mcp_server.py
  vectorstore.py
ui.py
requirements.txt
README.md
```

---

## Improvements

- **Smarter memory**  
  - Replace full‑history context with summarization  
  - Add semantic memory (vectorstore) for long‑term facts  
  - Separate system, memory, retrieved docs, and recent messages  

- **Streaming responses**  
  - Switch UI to `HTTPClient` for token‑level streaming  
  - Improve immediacy and reduce perceived latency  

- **Document‑aware context**  
  - Inject retrieved chunks directly into workflow context  
  - Show retrieved docs in sidebar  
  - Cache relevant passages across turns  

- **Tool selection UI**  
  - Let users choose SQL, Docs, or Workflow tools manually 
  - Let users proofread SQL code before execution

- **Multi‑session support**  
  - Named sessions  
  - Save/load past conversations  
  - Export chat logs
