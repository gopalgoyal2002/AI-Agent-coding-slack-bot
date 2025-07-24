from openai import OpenAI

client = OpenAI()

def planner_node(state):
    if not isinstance(state, dict):
        state = state.dict()

    query = state.get("query", "")
    chat_history = state.get("chat_history", [])

    # Add user message
    chat_history.append({"role": "user", "content": query})

    # You can add system or assistant messages too if needed
    messages = [{"role": "system", "content": "You are a planner..."}] + chat_history

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    llm_output = response.choices[0].message.content.lower()
    decision = "code" if "code" in llm_output else "llm"

    # Append assistant's response to chat history
    chat_history.append({"role": "assistant", "content": response.choices[0].message.content})

    state["decision"] = decision
    state["chat_history"] = chat_history

    return state
