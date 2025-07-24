
# 🤖 LangGraph AI Agent

An autonomous AI agent built using **LangGraph**, **OpenAI**, and **Slack integration**. It processes user queries, decides whether to respond directly using LLM or write and execute Python code dynamically, and finally notifies results to Slack.

## 🔧 Features

- 🔍 **Planner Node**: Uses OpenAI to decide if the task requires code or direct LLM response.
- ⚙️ **Executor Node**: 
  - If decision is `"llm"` → responds directly using GPT-4o.
  - If decision is `"code"` → asks GPT-4o to generate code, executes it, and captures the output or error.
- 💬 **Slack Notifier Node**: Sends the final output to a configured Slack channel via local MCP server.
- 🔁 **Retry mechanism**: If code execution fails, it routes back to planner for a retry.
- 💡 **LangGraph** handles the orchestration and conditional transitions.

---

## 📂 Project Structure

```
ai_agent_project/
│
├── nodes/
│   ├── planner_node.py       # Decides LLM or code generation
│   ├── executor_node.py      # Executes logic or code
│   └── slack_notifier.py     # Sends results to Slack
│
├── graph.py                  # LangGraph state machine
├── main.py                   # Entry point for user queries
└── temp.py                   # (Temporary) auto-generated code execution
```

---

## 🚀 How It Works

1. **User Input**: A query is taken from the user.
2. **Planner Node**:
   - Uses OpenAI to analyze the query.
   - Decides between `llm` or `code`.
3. **Executor Node**:
   - If `llm`: responds directly via GPT-4o.
   - If `code`: GPT-4o generates minimal Python code, saves to `temp.py`, and executes.
   - Catches stdout or error.
4. **Slack Notifier Node**:
   - Sends final result (or failure message) to a Slack channel via `POST /slack/send`.

---

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/langgraph-ai-agent.git
cd langgraph-ai-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Example `requirements.txt`:**

```text
openai
requests
langgraph
pydantic
```

### 3. Configure Environment

Ensure your OpenAI key is available as an environment variable:

```bash
export OPENAI_API_KEY=your_openai_key
```

(Optional) Start your local Slack MCP server (must expose `POST /slack/send`).

---

## ▶️ Running the Agent

```bash
python main.py
```

Sample prompt:

```bash
Enter your query: write a python program that prints fibonacci sequence
```

---

## ✅ Example Flow

```text
User Query: write a python program that prints fibonacci
↓
Planner decides: "code"
↓
LLM generates Python code
↓
Code executed successfully
↓
Output: 0 1 1 2 3 5 ...
↓
Slack notified ✅
```

---

## 🧠 Powered By

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [OpenAI](https://platform.openai.com/)
- Slack (via your own local or remote webhook/MCP)

---

## 📌 Notes

- This agent uses a retry mechanism: if code generation fails, it loops back to planner.
- Works best with clear, simple prompts that can be converted into minimal Python tasks.
- For production use, consider securing and validating the Slack endpoint and sandboxing code execution.

---

## 📤 Sample Slack Payload (from `slack_notifier.py`)

```json
{
  "query": "Your final output string",
  "type": "message",
  "destination": "slack"
}
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

---

## 📜 License

MIT License

---

## 🧪 Example Use Cases

- Convert queries like “sort a list in Python” into executable scripts.
- Automatically respond to technical questions with either explanation or code.
- Integrate with GitHub or Supabase in future for multi-service agent flows.

---

## 🙋‍♂️ Maintainer

**Gopal Goyal**  
[LinkedIn](https://www.linkedin.com/in/gopal-goyal-863981175/) | [GitHub](https://github.com/gopalgoyal2002)
