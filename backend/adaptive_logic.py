# backend/adaptive_logic.py

def adjust_difficulty(recent_logs):
    """
    Adjust difficulty based on recent answers and emotions.

    Args:
        recent_logs (list): List of recent performance documents from MongoDB.

    Returns:
        str: One of "increase", "decrease", or "maintain"
    """

    if not recent_logs:
        return "maintain"

    correct_count = sum(1 for log in recent_logs if log.get("correct"))
    confused_count = sum(1 for log in recent_logs if log.get("emotion") == "😕")

    if correct_count >= 3 and confused_count == 0:
        return "increase"
    elif confused_count >= 2 or correct_count <= 1:
        return "decrease"
    else:
        return "maintain"
