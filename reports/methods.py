from pathlib import Path

import matplotlib
from django.conf import settings

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def plot_counts(*, values: dict[str, int], filename: str, title: str) -> None:
    output_path = Path(settings.MEDIA_ROOT) / "reports" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(8, 5.25), facecolor="#FFFFFF")
    labels, counts = list(values.keys()), list(values.values())
    palette = ["#04055B", "#2596BE", "#6270C9", "#0D6B8C"]
    colors = [palette[index % len(palette)] for index in range(len(labels))]
    axis.bar(labels, counts, color=colors, edgecolor="#04055B", linewidth=0.8)
    axis.set_facecolor("#FFFFFF")
    axis.set_xlabel("Categorías", color="#04055B", fontweight="bold")
    axis.set_ylabel("Lecturas", color="#04055B", fontweight="bold")
    axis.set_title(title, color="#04055B", fontweight="bold", pad=16)
    axis.grid(axis="y", alpha=0.18, color="#04055B")
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)
    axis.tick_params(axis="x", colors="#000000", rotation=18)
    axis.tick_params(axis="y", colors="#000000")
    figure.tight_layout()
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(figure)
