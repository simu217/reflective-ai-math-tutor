# backend/sentiment_analysis.py

def interpret_emoji(emoji):
    """
    Converts an emoji into a standardized emotion label.

    Args:
        emoji (str): Emoji input from the user

    Returns:
        str: Emotion label
    """
    emoji_map = {
        "😊": "confident",
        "😕": "confused",
        "😠": "frustrated",
        "😐": "neutral"
    }
    return emoji_map.get(emoji.strip(), "unknown")


def interpret_text(feedback):
    """
    Interprets written feedback and maps it to an emotional label.

    Args:
        feedback (str): User input describing how they feel

    Returns:
        str: Emotion label
    """
    text = feedback.lower()
    if "confident" in text or "easy" in text or "got it" in text:
        return "confident"
    elif "confused" in text or "don't understand" in text or "not sure" in text:
        return "confused"
    elif "angry" in text or "hard" in text or "frustrated" in text:
        return "frustrated"
    else:
        return "neutral"
