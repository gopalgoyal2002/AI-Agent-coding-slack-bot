import requests

def notify_slack(state):
    print("[Slack Notifier] Received state:", state)
    
    if not isinstance(state, dict):
        state = state.dict()

    result = state.get("result", "")
    if not result.strip():
        result = "No result to send"

    print("[Slack Notifier] Sending to Slack:", result)

    payload = {
        "query": result,
        "type": "message",
        "destination": "slack"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("http://localhost:8000/slack/send", json=payload, headers=headers)
        print(f"[Slack Notifier] Slack responded with status: {response.status_code}")
        print(f"[Slack Notifier] Slack response content: {response.text}")
        notified = response.status_code == 200
    except Exception as e:
        print("[Slack Notifier] Error sending to Slack:", e)
        notified = False

    state["notified"] = notified
    return state
