import time

def timeit(fn):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        latency = round(time.perf_counter() - start, 3)
        return result, latency
    return wrapper

def trim_history(history, max_turns):
    return history[-max_turns:] if len(history) > max_turns else history

def format_messages(history, system_prompt):
    messages = [{"role": "system", "content": system_prompt}]
    for user, assistant in history:
        messages.append({"role": "user", "content": user})
        if assistant:
            messages.append({"role": "assistant", "content": assistant})
    return messages