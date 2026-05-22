import sys, os, csv, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from shared.config import SYSTEM_PROMPT
from oss_assistant.model import generate as oss_generate
from frontier_assistant.model import generate as frontier_generate
from evaluation.prompts import FACTUAL_PROMPTS, ADVERSARIAL_PROMPTS, BIAS_PROMPTS

os.makedirs("evaluation/results", exist_ok=True)

def run_single(prompt, model_fn):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    start = time.perf_counter()
    response = model_fn(messages)
    latency = round(time.perf_counter() - start, 3)
    return response, latency

def run_all():
    all_prompts = (
        [(p["prompt"], "factual") for p in FACTUAL_PROMPTS] +
        [(p, "adversarial") for p in ADVERSARIAL_PROMPTS] +
        [(p, "bias") for p in BIAS_PROMPTS]
    )
    rows = []
    for prompt, category in all_prompts:
        print(f"Testing [{category}]: {prompt[:60]}...")
        oss_resp, oss_lat = run_single(prompt, oss_generate)
        frontier_resp, frontier_lat = run_single(prompt, frontier_generate)
        rows.append({
            "category": category,
            "prompt": prompt,
            "oss_response": oss_resp,
            "oss_latency": oss_lat,
            "frontier_response": frontier_resp,
            "frontier_latency": frontier_lat,
        })
    with open("evaluation/results/raw_responses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print("Done. Saved to evaluation/results/raw_responses.csv")

if __name__ == "__main__":
    run_all()