import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np

os.makedirs("evaluation/results", exist_ok=True)

df = pd.read_csv("evaluation/results/scores.csv")

metrics = ["accuracy", "safety", "bias"]
oss_avg    = [df[f"oss_{m}"].mean() for m in metrics]
frt_avg    = [df[f"frontier_{m}"].mean() for m in metrics]
oss_lat    = df["oss_latency"].astype(float).mean()
frt_lat    = df["frontier_latency"].astype(float).mean()
categories = df["category"].unique()
oss_cat    = [df[df["category"]==c][[f"oss_{m}" for m in metrics]].mean().mean() for c in categories]
frt_cat    = [df[df["category"]==c][[f"frontier_{m}" for m in metrics]].mean().mean() for c in categories]

OSS_COLOR = "#7C3AED"
FRT_COLOR = "#059669"
BG        = "#0f0f1a"
CARD      = "#1a1a2e"
TEXT      = "#e2e8f0"
MUTED     = "#64748b"

fig = plt.figure(figsize=(14, 10), facecolor=BG)
fig.suptitle(
    "AI Assistant Evaluation Report — OSS vs Frontier",
    fontsize=18, fontweight="bold", color=TEXT, y=0.97
)

gs = GridSpec(2, 3, figure=fig, hspace=0.55, wspace=0.4,
              left=0.07, right=0.97, top=0.90, bottom=0.08)

# Chart 1: Overall scores
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(CARD)
x  = np.arange(len(metrics))
w  = 0.32
b1 = ax1.bar(x - w/2, oss_avg, w, color=OSS_COLOR, zorder=3)
b2 = ax1.bar(x + w/2, frt_avg, w, color=FRT_COLOR, zorder=3)
ax1.set_xticks(x)
ax1.set_xticklabels(["Accuracy", "Safety", "Bias\nAvoidance"], color=TEXT, fontsize=9)
ax1.set_ylim(0, 10)
ax1.set_title("Scores by Dimension", color=TEXT, fontsize=11, pad=10)
ax1.set_ylabel("Score (0-10)", color=MUTED, fontsize=8)
ax1.tick_params(colors=MUTED, labelsize=8)
ax1.spines[:].set_color(MUTED)
ax1.spines[:].set_alpha(0.2)
ax1.yaxis.grid(True, color=MUTED, alpha=0.15, zorder=0)
ax1.set_axisbelow(True)
for bar in b1:
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.15,
             f"{bar.get_height():.1f}", ha="center", color=TEXT, fontsize=7.5)
for bar in b2:
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.15,
             f"{bar.get_height():.1f}", ha="center", color=TEXT, fontsize=7.5)

# Chart 2: By category
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(CARD)
x2 = np.arange(len(categories))
b3 = ax2.bar(x2 - w/2, oss_cat, w, color=OSS_COLOR, zorder=3)
b4 = ax2.bar(x2 + w/2, frt_cat, w, color=FRT_COLOR, zorder=3)
ax2.set_xticks(x2)
ax2.set_xticklabels([c.capitalize() for c in categories], color=TEXT, fontsize=9)
ax2.set_ylim(0, 10)
ax2.set_title("Scores by Category", color=TEXT, fontsize=11, pad=10)
ax2.set_ylabel("Avg Score (0-10)", color=MUTED, fontsize=8)
ax2.tick_params(colors=MUTED, labelsize=8)
ax2.spines[:].set_color(MUTED)
ax2.spines[:].set_alpha(0.2)
ax2.yaxis.grid(True, color=MUTED, alpha=0.15, zorder=0)
ax2.set_axisbelow(True)
for bar in b3:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.15,
             f"{bar.get_height():.1f}", ha="center", color=TEXT, fontsize=7.5)
for bar in b4:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.15,
             f"{bar.get_height():.1f}", ha="center", color=TEXT, fontsize=7.5)

# Chart 3: Latency
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(CARD)
bars = ax3.bar(["OSS\n(Qwen2.5)", "Frontier\n(Llama3)"],
               [oss_lat, frt_lat],
               color=[OSS_COLOR, FRT_COLOR], width=0.45, zorder=3)
ax3.set_title("Avg Response Latency", color=TEXT, fontsize=11, pad=10)
ax3.set_ylabel("Seconds", color=MUTED, fontsize=8)
ax3.tick_params(colors=TEXT, labelsize=9)
ax3.spines[:].set_color(MUTED)
ax3.spines[:].set_alpha(0.2)
ax3.yaxis.grid(True, color=MUTED, alpha=0.15, zorder=0)
ax3.set_axisbelow(True)
for bar, val in zip(bars, [oss_lat, frt_lat]):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
             f"{val:.2f}s", ha="center", color=TEXT, fontsize=10, fontweight="bold")

# Chart 4: Radar
ax4 = fig.add_subplot(gs[1, 0], polar=True)
ax4.set_facecolor(CARD)
radar_labels = ["Accuracy", "Safety", "Bias\nAvoidance", "Speed*"]
max_lat      = max(oss_lat, frt_lat) if max(oss_lat, frt_lat) > 0 else 1
oss_speed    = round(10 * (1 - oss_lat / max_lat), 1)
frt_speed    = round(10 * (1 - frt_lat / max_lat), 1)
oss_vals_r   = oss_avg + [oss_speed]
frt_vals_r   = frt_avg + [frt_speed]
N            = len(radar_labels)
angles       = [n / float(N) * 2 * np.pi for n in range(N)]
angles      += angles[:1]
oss_vals_r  += oss_vals_r[:1]
frt_vals_r  += frt_vals_r[:1]
ax4.plot(angles, oss_vals_r, color=OSS_COLOR, linewidth=2)
ax4.fill(angles, oss_vals_r, color=OSS_COLOR, alpha=0.25)
ax4.plot(angles, frt_vals_r, color=FRT_COLOR, linewidth=2)
ax4.fill(angles, frt_vals_r, color=FRT_COLOR, alpha=0.25)
ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(radar_labels, color=TEXT, fontsize=8)
ax4.set_ylim(0, 10)
ax4.set_yticks([2, 4, 6, 8, 10])
ax4.set_yticklabels(["2","4","6","8","10"], color=MUTED, fontsize=6)
ax4.grid(color=MUTED, alpha=0.2)
ax4.spines["polar"].set_color(MUTED)
ax4.spines["polar"].set_alpha(0.2)
ax4.set_facecolor(CARD)
ax4.set_title("Overall Radar", color=TEXT, fontsize=11, pad=15)

# Chart 5: Win rate pie
ax5 = fig.add_subplot(gs[1, 1])
ax5.set_facecolor(CARD)
all_scores = []
for _, row in df.iterrows():
    oss_s = (row["oss_accuracy"] + row["oss_safety"] + row["oss_bias"]) / 3
    frt_s = (row["frontier_accuracy"] + row["frontier_safety"] + row["frontier_bias"]) / 3
    if oss_s > frt_s:
        all_scores.append("OSS")
    elif frt_s > oss_s:
        all_scores.append("Frontier")
    else:
        all_scores.append("Tie")
oss_wins = all_scores.count("OSS")
frt_wins = all_scores.count("Frontier")
ties     = all_scores.count("Tie")
pie_vals   = [v for v in [oss_wins, frt_wins, ties] if v > 0]
pie_labels = []
pie_colors = []
if oss_wins > 0:
    pie_labels.append(f"OSS wins\n({oss_wins})")
    pie_colors.append(OSS_COLOR)
if frt_wins > 0:
    pie_labels.append(f"Frontier wins\n({frt_wins})")
    pie_colors.append(FRT_COLOR)
if ties > 0:
    pie_labels.append(f"Ties\n({ties})")
    pie_colors.append("#475569")
wedges, texts, autotexts = ax5.pie(
    pie_vals, labels=pie_labels, colors=pie_colors,
    autopct="%1.0f%%", startangle=90,
    textprops={"color": TEXT, "fontsize": 8},
    wedgeprops={"linewidth": 1, "edgecolor": BG}
)
for at in autotexts:
    at.set_color(TEXT)
    at.set_fontsize(8)
ax5.set_title("Head-to-Head Win Rate", color=TEXT, fontsize=11, pad=10)

# Chart 6: Summary table
ax6 = fig.add_subplot(gs[1, 2])
ax6.set_facecolor(CARD)
ax6.axis("off")
oss_overall = np.mean(oss_avg)
frt_overall = np.mean(frt_avg)
table_data = [
    ["Metric",         "OSS",                    "Frontier"],
    ["Accuracy",       f"{oss_avg[0]:.1f}/10",   f"{frt_avg[0]:.1f}/10"],
    ["Safety",         f"{oss_avg[1]:.1f}/10",   f"{frt_avg[1]:.1f}/10"],
    ["Bias Avoidance", f"{oss_avg[2]:.1f}/10",   f"{frt_avg[2]:.1f}/10"],
    ["Avg Latency",    f"{oss_lat:.2f}s",         f"{frt_lat:.2f}s"],
    ["Overall",        f"{oss_overall:.1f}/10",   f"{frt_overall:.1f}/10"],
    ["Cost",           "Free",                    "Free (Groq)"],
    ["Privacy",        "Local",                   "API call"],
]
tbl = ax6.table(
    cellText=table_data[1:],
    colLabels=table_data[0],
    cellLoc="center",
    loc="center",
    bbox=[0, 0.05, 1, 0.9],
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
for (row, col), cell in tbl.get_celld().items():
    cell.set_facecolor(CARD)
    cell.set_edgecolor(MUTED)
    cell.set_alpha(0.3)
    if row == 0:
        cell.set_facecolor("#1e293b")
        cell.set_text_props(color=TEXT, fontweight="bold")
    elif col == 1:
        cell.set_text_props(color="#a78bfa")
    elif col == 2:
        cell.set_text_props(color="#34d399")
    else:
        cell.set_text_props(color=TEXT)
ax6.set_title("Summary Table", color=TEXT, fontsize=11, pad=10)

# Legend
legend_patches = [
    mpatches.Patch(color=OSS_COLOR, label="OSS — Qwen2.5-0.5B (local)"),
    mpatches.Patch(color=FRT_COLOR, label="Frontier — Llama3.3-70B (Groq)"),
]
fig.legend(
    handles=legend_patches,
    loc="lower center",
    ncol=2,
    fontsize=9,
    facecolor=CARD,
    edgecolor=MUTED,
    labelcolor=TEXT,
    bbox_to_anchor=(0.5, 0.01),
)

# Recommendations
fig.text(
    0.5, 0.045,
    "Recommendations:  Use Frontier for accuracy tasks  |  Use OSS for private/offline deployments  |  Deploy OSS on GPU to reduce latency",
    ha="center", color=MUTED, fontsize=8, style="italic"
)

# Save only as PNG (avoids PDF permission errors)
out_png = "evaluation/results/evaluation_report.png"
plt.savefig(out_png, dpi=180, bbox_inches="tight", facecolor=BG)
print(f"Report saved: {out_png}")
plt.close()