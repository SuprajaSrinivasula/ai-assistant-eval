from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from shared .config import OSS_MODEL_NAME, MAX_NEW_TOKENS
import torch

_pipe = None

def load_model():
    global _pipe
    if _pipe is None:
        print(f"Loading {OSS_MODEL_NAME}...")
        tokenizer = AutoTokenizer.from_pretrained(OSS_MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            OSS_MODEL_NAME,
            torch_dtype=torch.float32,
            device_map="auto"
        )
        _pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            temperature=0.7,
        )
    return _pipe

def generate(messages: list[dict]) -> str:
    pipe = load_model()
    text = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    output = pipe(text)
    generated = output[0]["generated_text"]
    return generated[len(text):].strip()