import subprocess
from openai import OpenAI
import re

def extract_python_code(text):
    """
    Extracts code from markdown code blocks or plain response.
    """
    # Match code blocks in triple backticks with optional "python"
    match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()  # fallback: return as-is

client = OpenAI()

def executor_node(state):
    print("[Executor Node] Input state:", state)

    # Convert Pydantic model to dict if needed
    if not isinstance(state, dict):
        state = state.dict()

    decision = state.get("decision")
    query = state.get("query")
    print(f"[Executor Node] Decision: {decision}, Query: {query}")

    result = None
    success = False

    if decision == "llm":
        chat_history = state.get("chat_history", [])
        chat_history.append({"role": "user", "content": query})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history
        )

        answer = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": answer})

        result = answer
        success = True
        state["chat_history"] = chat_history

        print(f"[Executor Node] LLM answered: {answer[:100]}...")

    else:
        print("[Executor Node] Generating code using LLM to solve the task.")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Write minimal Python code to solve the following task:"},
                {"role": "user", "content": query}
            ]
        )
        code = response.choices[0].message.content.strip("```python").strip("```")
        print("[Executor Node] Generated code:\n", code)

        clean_code = extract_python_code(code)
        with open("temp.py", "w") as f:
            f.write(clean_code)

        try:
            result_bytes = subprocess.check_output(["python", "temp.py"], stderr=subprocess.STDOUT, timeout=10)
            result = result_bytes.decode()
            success = True
            print("[Executor Node] Code executed successfully. Output:", result)
        except subprocess.CalledProcessError as e:
            result = e.output.decode()
            success = False
            print("[Executor Node] Code execution failed. Error output:", result)
        except subprocess.TimeoutExpired:
            result = "Execution timed out."
            success = False
            print("[Executor Node] Code execution timed out.")
        except Exception as e:
            result = f"Unexpected error: {e}"
            success = False
            print(f"[Executor Node] Unexpected error during code execution: {e}")

    state["result"] = result
    state["success"] = success

    return state
