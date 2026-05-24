#  AI Assistant Evaluation — OSS vs Frontier

A professional side-by-side comparison of two AI assistants:
- **OSS Assistant** — Qwen2.5-0.5B-Instruct running locally
- **Frontier Assistant** — Llama 3.3 70B via Groq API

Evaluated across **Hallucination Rate**, **Bias & Harmful Outputs**, and **Content Safety**.

---

##  Preview

| OSS Assistant | Frontier Assistant |
|:---:|:---:|
| Qwen2.5 · Local · Free | Llama 3.3 70B · Groq · Ultra Fast |
| `localhost:7860` | `localhost:7862` |

---

##  Project Structure
ai-assistant-eval/
├── oss_assistant/
│   ├── app.py              # Gradio UI — dark themed chat interface
│   ├── model.py            # Qwen2.5 model loader (HuggingFace)
│   └── guardrails.py       # Input safety filtering layer
│
├── frontier_assistant/
│   ├── app.py              # Gradio UI — dark themed chat interface
│   └── model.py            # Llama 3.3 70B via Groq API client
│
├── evaluation/
│   ├── prompts.py          # 16 test prompts across 3 categories
│   ├── runner.py           # Runs both models on all prompts
│   ├── judge.py            # LLM-as-judge scoring (0-10 per dimension)
│   ├── report.py           # Generates 6-chart infographic report
│   └── results/
│       ├── raw_responses.csv
│       ├── scores.csv
│       └── evaluation_report.png
│
├── shared/
│   ├── config.py           # Global constants and settings
│   └── utils.py            # Shared helper functions
│
├── hf_space/               # Hugging Face Spaces deployment (bonus)
├── .env.example            # Environment variable template
├── requirements.txt        # All Python dependencies
└── README.md

---

##  Setup Instructions

### Prerequisites
- Python 3.11+
- Git
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repository

```bash
git clone https://github.com/SuprajaSrinivasula/ai-assistant-eval.git
cd ai-assistant-eval
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
```

Get your free keys:
- **Groq** (no credit card): https://console.groq.com
- **Langfuse** (observability): https://cloud.langfuse.com

### 5. Run the assistants

Open two terminals:

```bash
# Terminal 1 — OSS Assistant
python -m oss_assistant.app
# Visit http://127.0.0.1:7860
```

```bash
# Terminal 2 — Frontier Assistant
python -m frontier_assistant.app
# Visit http://127.0.0.1:7862
```

### 6. Run the evaluation pipeline

```bash
# Collect responses from both models
python -m evaluation.runner

# Score all responses using LLM-as-judge
python -m evaluation.judge

# Generate infographic comparison report
python -m evaluation.report
```

Output saved to `evaluation/results/evaluation_report.png`

---

##  Architecture Decisions

### Why Qwen2.5-0.5B for OSS?
- Smallest model that still follows instructions reliably
- Runs entirely on CPU — no GPU required
- Has a proper chat template for multi-turn conversations
- First run downloads ~1GB weights, cached locally after that

### Why Llama 3.3 70B via Groq?
- Groq offers a **completely free tier** with no credit card needed
- Llama 3.3 70B matches GPT-4 class performance on most benchmarks
- Groq's LPU hardware delivers sub-second latency (~0.3–1s)
- Makes the latency comparison in the eval report dramatic and clear

### Why Gradio for the UI?
- Both assistants use **identical UI structure** — fair comparison
- Built-in chat history management for multi-turn memory
- Rapid prototyping without frontend code

### Why LLM-as-judge for evaluation?
- Static benchmarks give pass/fail — LLM-as-judge gives nuanced 0–10 scores with reasoning
- Can evaluate subjective qualities like bias and tone
- Scales easily to new prompt categories

---

##  Tradeoffs

| | OSS (Qwen2.5) | Frontier (Llama 3.3 70B) |
|:---|:---:|:---:|
| **Cost** | Free forever | Free (Groq rate limits) |
| **Privacy** | 100% local | Data sent to Groq API |
| **Latency** | 5–15s (CPU) | 0.3–1s (Groq LPU) |
| **Response quality** | Good for simple tasks | Consistently stronger |
| **Offline use** |  Yes |  No |
| **Setup complexity** | High (1GB download) | Low (API key only) |
| **Customizable** | Fine-tunable |  API only |
| **Guardrails** | Shared layer | Shared layer |

---

##  Evaluation Results

Three prompt categories — 16 prompts total:

### Prompt Categories

| Category | Count | Tests For |
|:---|:---:|:---|
| **Factual** | 6 | Hallucination rate, accuracy on real-world knowledge |
| **Adversarial** | 5 | Jailbreak resistance, prompt injection defense |
| **Bias** | 5 | Stereotypes, discrimination, political neutrality |

### Scoring Method

Each response scored 0–10 on three dimensions by an LLM judge:

- `accuracy` — Is the response factually correct?
- `safety` — Did it handle harmful requests appropriately?
- `bias` — Is the response free of stereotypes and discrimination?

### Key Findings

- **Frontier model** consistently outperforms OSS on accuracy and safety
- **OSS model** is surprisingly competitive on bias avoidance
- **Latency gap** is significant: OSS averages 10x slower on CPU
- Both models **refused adversarial prompts** when guardrails were active

---

##  What I Would Improve With More Time

1. **Streaming responses** — Token-by-token streaming for better UX
2. **Vector memory** — ChromaDB for long-term memory across sessions
3. **Tool use** — Web search, calculator, code execution via function calling
4. **GPU deployment** — Modal A10G GPU for 10x faster OSS inference
5. **Fine-tuning** — Domain-specific fine-tune to close the quality gap
6. **Larger eval set** — Expand to 100+ prompts using TruthfulQA and AdvBench
7. **Human eval UI** — Blind A/B comparison interface for human raters
8. **CI/CD pipeline** — Automated eval runs on every GitHub push

---

##  Bonus: Hugging Face Deployment

The OSS assistant is deployed publicly on Hugging Face Spaces:

>  **Live Demo**: [huggingface.co/spaces/SuprajaSrinivasula/ai-oss-assistant](https://huggingface.co/spaces/SuprajaSrinivasula/ai-oss-assistant)

### Cost & Latency Table

| Platform | Model | Avg Latency | Cost/1K tokens | Monthly est. |
|:---|:---|:---:|:---:|:---:|
| HF Spaces (CPU free) | Qwen2.5-0.5B | ~10–15s | $0.00 | $0 |
| Modal (A10G GPU) | Qwen2.5-0.5B | ~0.8–1.5s | ~$0.0003 | ~$15 |
| Groq API | Llama 3.3 70B | ~0.3–1s | $0.00 (free tier) | $0 |

---

##  Tech Stack

| Component | Technology |
|:---|:---|
| OSS Model | Qwen2.5-0.5B-Instruct (HuggingFace) |
| Frontier Model | Llama 3.3 70B (Groq API) |
| UI Framework | Gradio 4.x |
| Evaluation | LLM-as-judge + custom prompts |
| Observability | Langfuse |
| Visualization | Matplotlib + Seaborn |
| Deployment | Hugging Face Spaces |

---

##  License

MIT License — free to use, modify, and distribute.

---

##  Author

**Srinivasula Subhadra Supraja**
Built as part of the Ollive Founding AI/ML Engineer evalution