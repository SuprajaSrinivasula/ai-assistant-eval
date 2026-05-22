import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from shared.config import SYSTEM_PROMPT, MAX_HISTORY_TURNS
from shared.utils import trim_history, format_messages, timeit
from frontier_assistant.model import generate
from oss_assistant.guardrails import is_safe_input

@timeit
def _generate_timed(messages):
    return generate(messages)

def respond(message, history):
    safe, reason = is_safe_input(message)
    if not safe:
        return reason

    history = trim_history(history, MAX_HISTORY_TURNS)
    messages = format_messages(history, SYSTEM_PROMPT)
    messages.append({"role": "user", "content": message})

    try:
        response, latency = _generate_timed(messages)
        print(f"[Frontier] latency={latency}s")
        return response
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.ChatInterface(
    fn=respond,
    title="Frontier Assistant (Claude)",
    description="Powered by Claude Sonnet via Anthropic API",
    examples=[
        "What is the capital of France?",
        "Explain quantum entanglement simply.",
        "Write a Python function to reverse a string.",
    ],
)

if __name__ == "__main__":
    demo.launch(server_port=7863
    )