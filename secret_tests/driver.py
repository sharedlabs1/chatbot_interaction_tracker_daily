import importlib.util
import datetime
import os
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    report_lines = [f"\n=== Chatbot Tracker Test Run at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ==="]

    visible_tests = [
        {
            "desc": "Registering a new chatbot user",
            "func": "register_user",
            "input": ({}, "John", "2024-03-17 10:00:00"),
            "expected": {"John": {"messages": 0, "last_interaction": "2024-03-17 10:00:00", "status": "Inactive"}}
        },
        {
            "desc": "Logging an interaction and updating the message count",
            "func": "log_interaction",
            "input": ({"John": {"messages": 0, "last_interaction": "2024-03-17 10:00:00", "status": "Inactive"}}, "John", "2024-03-17 12:30:00"),
            "expected": {"John": {"messages": 1, "last_interaction": "2024-03-17 12:30:00", "status": "Inactive"}}
        },
        {
            "desc": "Retrieving active users based on message count",
            "func": "get_active_users",
            "input": {"John": {"messages": 1, "last_interaction": "2024-03-17 12:30:00", "status": "Inactive"}},
            "expected": []
        }
    ]

    hidden_tests = [
        {
            "desc": "Generating an engagement report based on user messages",
            "func": "generate_engagement_report",
            "input": {
                "John": {"messages": 6, "last_interaction": "2024-03-17 12:30:00", "status": "Inactive"},
                "Alice": {"messages": 12, "last_interaction": "2024-03-17 11:00:00", "status": "Active"},
                "Bob": {"messages": 20, "last_interaction": "2024-03-17 09:45:00", "status": "Active"}
            },
            "expected": {
                "John": "Moderate Engagement",
                "Alice": "Moderate Engagement",
                "Bob": "High Engagement"
            }
        },
        {
            "desc": "Handling interactions for non-existent users",
            "func": "log_interaction",
            "input": ({}, "Alice", "2024-03-17 11:00:00"),
            "expected": "Error: User not found"
        }
    ]

    edge_rules = {
        "register_user": ["'messages'", "'last_interaction'", "'Inactive'"],
        "log_interaction": ["+=", "'last_interaction'", "if"],
        "get_active_users": ["for", "if", "append"],
        "generate_engagement_report": ["if", "elif", "else"]
    }

    def check_edge_case(func_name):
        func = getattr(student_module, func_name)
        try:
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()
        except Exception:
            return "Function not found"

        if 'pass' in src and len(src) < 80:
            return "Function contains only 'pass'"
        if 'return' in src and len(src) < 120 and "{" in src:
            return "Hardcoded return"
        for keyword in edge_rules.get(func_name, []):
            if keyword not in src:
                return f"Missing keyword or logic: `{keyword}`"
        return None

    def run_tests(test_cases, section_name):
        for idx, case in enumerate(test_cases, 1):
            reason = check_edge_case(case["func"])
            try:
                func = getattr(student_module, case["func"])
                result = func(*case["input"]) if isinstance(case["input"], tuple) else func(case["input"])
                passed = result == case["expected"]
                if passed and not reason:
                    msg = f"✅ {section_name} Test Case {idx} Passed: {case['desc']}"
                else:
                    msg = f"❌ {section_name} Test Case {idx} Failed: {case['desc']} | Reason: {reason or 'Output mismatch'}"
            except Exception as e:
                msg = f"❌ {section_name} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    run_tests(visible_tests, "Visible")
    run_tests(hidden_tests, "Hidden")

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
