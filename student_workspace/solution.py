# student_workspace/solution.py

def register_user(chat_data: dict, user_name: str, timestamp: str) -> dict:
    if user_name in chat_data:
        return "Error: User already exists"
    chat_data[user_name] = {
        "messages": 0,
        "last_interaction": timestamp,
        "status": "Inactive"
    }
    return chat_data


def log_interaction(chat_data: dict, user_name: str, timestamp: str) -> dict:
    if user_name not in chat_data:
        return "Error: User not found"
    
    chat_data[user_name]["messages"] += 1
    chat_data[user_name]["last_interaction"] = timestamp
    
    if chat_data[user_name]["messages"] > 10:
        chat_data[user_name]["status"] = "Active"
    
    return chat_data


def get_active_users(chat_data: dict) -> list:
    active_users = []
    for user, info in chat_data.items():
        if info.get("status") == "Active":
            active_users.append(user)
    return active_users


def generate_engagement_report(chat_data: dict) -> dict:
    report = {}
    for user, info in chat_data.items():
        messages = info.get("messages", 0)
        if messages < 5:
            report[user] = "Low Engagement"
        elif 5 <= messages <= 15:
            report[user] = "Moderate Engagement"
        else:
            report[user] = "High Engagement"
    return report
