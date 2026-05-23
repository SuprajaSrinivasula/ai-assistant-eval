AI Assistant Evaluation Framework
An AI assistant evaluation framework comparing an Open Source Assistant (Qwen2.5) with a Frontier Model Assistant (Groq Llama 3.3) across hallucination, bias, and safety benchmarks.

Project Overview

This project builds and evaluates two AI-powered personal assistants:
Open Source Assistant
Model: Qwen2.5-0.5B-Instruct
Runs locally using Hugging Face Transformers
Frontier Assistant
Model: Llama 3.3 70B via Groq API
Hosted inference using GroqCloud

The project compares both assistants on:
Hallucination rate, 
Bias & harmful outputs, 
Content safety, 
Response latency, 
Assistant behavior,
Features, 
Multi-turn conversation support,
Short-term conversational memory,
Gradio chat interface,
Open-source model inference,
Frontier hosted model inference,
Safety guardrails,
Evaluation scripts,
Deployment-ready structure

Tech Stack
Component	Technology,
Language	Python,
UI	Gradio,
OSS Model	Qwen2.5-0.5B-Instruct,
Frontier Model	Groq Llama 3.3 70B,
Framework	Hugging Face Transformers,
API Provider	Groq,
Deployment	Hugging Face Spaces.

Project Structure
ai-assistant-eval/
│
├── oss_assistant/
│   ├── app.py
│   ├── model.py
│   ├── guardrails.py
│   └── __init__.py
│
├── frontier_assistant/
│   ├── app.py
│   ├── model.py
│   └── __init__.py
│
├── evaluation/
│
├── deployment/
│
├── requirements.txt
├── README.md
├── .env

Installation

1. Clone Repository

git clone https://github.com/SuprajaSrinivasula/ai-assistant-eval.git

cd ai-assistant-eval

2. Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Linux/Mac
python -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt
Environment Variables

Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key
Running the Open Source Assistant
python -m oss_assistant.app

Runs on:
http://127.0.0.1:7860
Running the Frontier Assistant
python -m frontier_assistant.app

Runs on:
http://127.0.0.1:7861

Models Used

Open Source Model,
Qwen2.5-0.5B-Instruct,,
Lightweight and optimized for deployment,
Frontier Model,
Llama 3.3 70B,
Accessed through Groq API,
Ultra-low latency inference,
Evaluation Metrics

The assistants are evaluated using:

Factual prompts,
Adversarial prompts,
Sensitive prompts,
Jailbreak attempts,
Metrics,
Metric	Description,
Hallucination Rate	Incorrect or fabricated responses,
Bias Score	Harmful or discriminatory outputs,
Safety	Resistance to unsafe prompts,
Latency	Response generation time,
Safety Guardrails.

Implemented:
Harmful prompt filtering,
Unsafe keyword detection,
Refusal handling,
Basic moderation logic,
Deployment.

The Open Source Assistant can be deployed using:

Hugging Face Spaces,
Modal,
Ollama,
RunPod,

Recommended:

Hugging Face Spaces,
Future Improvements,
Long-term memory support,
RAG integration,
Advanced observability,
Tool calling,
Agent workflows,
Better evaluation automation,

Streaming responses


Demo

https://huggingface.co/spaces/srinivasula/ai-oss-assistant

Author
Srinivasula Subhadra Supraja
