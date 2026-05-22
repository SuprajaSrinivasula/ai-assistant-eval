import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("evaluation/results/scores.csv")

metrics = ["accuracy", "safety", "bias"]
oss_avg = [df[f"oss_{m}"].mean() for m in metrics]
frontier_avg = [df[f"frontier_{m}"].mean() for m in metrics]
oss_lat = df["oss_latency"].astype(float).mean()
frontier_lat = df["frontier_latency"].astype(float).mean()

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("OSS vs Frontier — Evaluation Results", fontsize=14, fontweight="bold")

x, w = np.arange(len(metrics)), 0.35

ax1 = axes[0]
ax1.bar(x - w/2, oss_avg, w, label="OSS (Qwen2.5)", color="#7F77DD")
ax1.bar(x + w/2, frontier_avg, w, label="Frontier (Claude)", color="#1D9E75")
ax1.set_xticks(x)
ax1.set_xticklabels(["Accuracy", "Safety", "Bias avoidance"])
ax1.set_ylim(0, 10)
ax1.set_title("Scores by dimension (0-10)")
ax1.legend()
ax1.grid(axis="y", alpha=0.3)

categories = df["category"].unique()
oss_cat = [df[df["category"]==c][[f"oss_{m}" for m in metrics]].mean().mean() for c in categories]
frt_cat = [df[df["category"]==c][[f"frontier_{m}" for m in metrics]].mean().mean() for c in categories]
x2 = np.arange(len(categories))
ax2 = axes[1]
ax2.bar(x2 - w/2, oss_cat, w, color="#7F77DD", label="OSS")
ax2.bar(x2 + w/2, frt_cat, w, color="#1D9E75", label="Frontier")
ax2.set_xticks(x2)
ax2.set_xticklabels(categories)
ax2.set_ylim(0, 10)
ax2.set_title("Avg score by category")
ax2.legend()
ax2.grid(axis="y", alpha=0.3)

ax3 = axes[2]
bars = ax3.bar(["OSS (Qwen2.5)", "Frontier (Claude)"],
               [oss_lat, frontier_lat], color=["#7F77DD", "#1D9E75"], width=0.5)
ax3.set_title("Avg response latency (s)")
ax3.grid(axis="y", alpha=0.3)
for bar, val in zip(bars, [oss_lat, frontier_lat]):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f"{val:.2f}s", ha="center")

plt.tight_layout()
plt.savefig("evaluation/results/evaluation_report.png", dpi=150, bbox_inches="tight")
plt.savefig("evaluation_report.pdf", bbox_inches="tight")
print("Report saved.")

if __name__ == "__main__":
    pass