from langgraph.graph import StateGraph, END
from nodes.planner_node import planner_node
from nodes.executor_node import executor_node
from nodes.slack_notifier import notify_slack
from pydantic import BaseModel
from typing import Optional

from typing import List

class StateSchema(BaseModel):
    query: str
    decision: Optional[str] = None
    result: Optional[str] = None
    success: Optional[bool] = None
    notified: Optional[bool] = None
    chat_history: List[dict] = [] 

builder = StateGraph(state_schema=StateSchema)

builder.add_node("planner", planner_node)
builder.add_node("executor", executor_node)
builder.add_node("slack", notify_slack)

builder.set_entry_point("planner")
builder.add_edge("planner", "executor")

builder.add_conditional_edges(
    "executor",
    lambda state: "success" if state.success else "retry",
    {
        "success": "slack",
        "retry": "planner"
    }
)

builder.add_edge("slack", END)

graph = builder.compile()
