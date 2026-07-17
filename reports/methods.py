from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from django.conf import settings


def plot_counts(*, values: dict[str, int], filename: str, title: str) -> None:
    output_path = Path(settings.MEDIA_ROOT) / "reports" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.bar(list(values.keys()), list(values.values()))
    axis.set_xlabel("Categorías")
    axis.set_ylabel("Cantidad")
    axis.set_title(title)
    figure.tight_layout()
    figure.savefig(output_path)
    plt.close(figure)
