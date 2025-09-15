"""Annotate colormap YAML files with provenance comments."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CMAP_DIR = REPO_ROOT / "colormaps"

COLORBREWER = {
    "Accent",
    "Dark2",
    "Paired",
    "Pastel1",
    "Pastel2",
    "Set1",
    "Set2",
    "Set3",
    "BrBG",
    "PiYG",
    "PRGn",
    "PuOr",
    "RdBu",
    "RdGy",
    "RdYlBu",
    "RdYlGn",
    "Spectral",
    "Blues",
    "Greens",
    "Reds",
    "Purples",
    "Oranges",
    "Greys",
    "YlOrBr",
    "YlOrRd",
    "OrRd",
    "PuRd",
    "RdPu",
    "BuPu",
    "GnBu",
    "PuBu",
    "YlGnBu",
    "PuBuGn",
    "BuGn",
    "YlGn",
}

APACHE_MAPS = {"turbo"}


def base_name(name: str) -> str:
    """Return the base token for a colormap file name."""
    return name.replace("_r256", "").replace("_r", "").replace("256", "")


def source_for(name: str) -> str:
    """Return a provenance string for *name*."""
    base = base_name(name)
    if base in COLORBREWER:
        return "ColorBrewer (https://colorbrewer2.org, Apache-2.0)"
    if base in APACHE_MAPS:
        return "Turbo (https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html, Apache-2.0)"
    return "Matplotlib (https://matplotlib.org/stable/project/license.html)"


def annotate_file(path: Path) -> None:
    """Insert provenance comments at the top of *path* if absent."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("# source:"):
        return
    source = source_for(path.stem)
    header = f"# source: {source}\n# palette: {path.stem}\n"
    path.write_text(header + text, encoding="utf-8")


def main() -> None:
    for yaml_path in CMAP_DIR.rglob("*.yaml"):
        annotate_file(yaml_path)


if __name__ == "__main__":
    main()
