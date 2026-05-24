BLOCKED_PATTERNS = [
    "ignore previous instructions", "you are now", "jailbreak",
    "act as dan", "do anything now", "no restrictions"
]
BLOCKED_TOPICS = [
    "make a bomb", "synthesize drugs", "hack into", "child abuse"
]

def is_safe_input(text: str) -> tuple[bool, str]:
    lower = text.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lower:
            return False, "I can't process that type of request."
    for topic in BLOCKED_TOPICS:
        if topic in lower:
            return False, "I'm not able to help with that."
    return True, ""