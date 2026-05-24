import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OSS_MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
FRONTIER_MODEL = "llama-3.3-70b-versatile"  # Groq's best model
MAX_HISTORY_TURNS = 10
MAX_NEW_TOKENS = 512
SYSTEM_PROMPT = "You are a helpful, harmless, and honest AI assistant."