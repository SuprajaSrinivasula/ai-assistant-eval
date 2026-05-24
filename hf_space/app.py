import gradio as gr
from model import generate

def respond(message, history):
    messages = []
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    
    messages.append({"role": "user", "content": message})
    response = generate(messages)
    return response

demo = gr.ChatInterface(
    fn=respond,
    title="OSS Assistant (Qwen2.5)",
    description="Powered by Qwen2.5-0.5B-Instruct",
    examples=[
        "What is the capital of France?",
        "Explain quantum entanglement simply.",
        "Write a Python function to reverse a string.",
    ],
)

if __name__ == "__main__":
    demo.launch(server_port=7861)
