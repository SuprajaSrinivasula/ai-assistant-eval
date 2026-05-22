import gradio as gr
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

def chat(message):
    result = pipe(message, max_new_tokens=100)
    return result[0]["generated_text"]

demo = gr.Interface(
    fn=chat,
    inputs="text",
    outputs="text",
    title="AI OSS Assistant"
)

demo.launch()