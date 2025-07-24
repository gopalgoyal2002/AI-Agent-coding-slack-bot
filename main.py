from graph import graph

if __name__ == "__main__":
    query = input("Enter your query: ")
    print(f"[Main] User query: {query}")

    state = {"query": query}

    final_state = graph.invoke(state)

    # final_state is a Pydantic model, convert to dict for easy printing
    print("[Main] Final state:", final_state)
    print("[Main] Final Result:", final_state.get("result", "No result"))
