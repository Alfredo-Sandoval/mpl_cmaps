## Matplotlib Colormaps (YAML)

Matplotlib-compatible colormaps encoded as simple YAML files plus a few helper tools to browse and preview them.


- `colormaps_explorer.html` — an interactive, client‑side explorer for quickly scanning palettes and their gradients.
- YAML colormap files (e.g., `viridis.yaml`, `Blues256.yaml`, …). Each file stores one palette under `palettes.custom.<NAME>` as a list of `R,G,B` strings.


## Picking CMAPS for Scientific Visualization

Picking a good colormap keeps plots honest and easy to read.

- Perceptually uniform first: Use ramps that get steadily lighter/darker with no odd hue jumps (e.g., `viridis`, `plasma`, `inferno`, `magma`, `cividis`, `turbo`). They hold up on screens and in print.
- Match the map to the data:
  - Sequential (low→high): single‑ or multi‑hue ramps with monotonic lightness (e.g., `Blues`, `Greens`, `Purples`, `YlOrRd`).
  - Diverging (around a reference like 0): true diverging maps with a neutral center (e.g., `coolwarm`, `RdBu`, `BrBG`, `PuOr`, `RdYlBu`). Set the midpoint to your reference.
  - Qualitative (categories): discrete palettes with clearly different hues (e.g., `tab10`, `tab20`, `Dark2`, `Set2`). Don’t use these for numeric ramps.
- grayscale/print: Make sure things still read in grayscale, or add labels/annotations. Perceptual ramps usually degrade nicely.
- Skip rainbows for numbers: `jet`, `rainbow`, `hsv`, and some `gist_*` maps aren’t uniform and can invent or hide features.
- show the scale: Add a colorbar with units; set sensible limits and note any nonlinear mapping (e.g., log). For diverging maps, center at the reference.

### 40k view

- Do: `viridis`, `plasma`, `inferno`, `magma`, `cividis`, `turbo` for general quantitative ramps.
- Do: `coolwarm`, `RdBu`, `BrBG`, `PiYG`, `PRGn` for signed deviations around zero.
- Do: `tab10`, `tab20`, `Dark2` for categories (≤10–20 groups).
- Caution: `hot`, `ocean`, `terrain`, `gist_ncar` — not perceptually uniform; use only when domain‑specific and well‑justified.
- Avoid (quantitative): `jet`, `rainbow`, `hsv` and similar.

## Layout

cmaps are grouped by purpose:

- `colormaps/perceptual/` — perceptually uniform sequential maps (good for viz).
- `colormaps/sequential/` — well‑behaved sequential maps (not strictly uniform but generally ok).
- `colormaps/diverging/` — diverging maps for +/- deviations.
- `colormaps/qualitative/` — qualitative/tabular sets for categories.
- `colormaps/non-uniform/` — legacy or rainbow‑like maps (avoid - jet included).
- `colormaps/other/` — everything else.

Notes

- Reversed variants (e.g., `_r` suffix) are kept with their base map. Many tools can reverse a cmap at runtime; easier then dupe files.
- `colormaps_explorer.html` reads an index file (`colormaps_index.json`) to load YAMLs from these folders.

## Refs

- Matplotlib Colormap Guide — https://matplotlib.org/stable/tutorials/colors/colormaps.html
- Smith, N. J., & van der Walt, S. (2015). A Better Default Colormap for Matplotlib (Viridis).
- Moreland, K. (2009–2016). Diverging Color Maps for Scientific Visualization — https://www.kennethmoreland.com/color-advice/
- Crameri, F., Shephard, G. E., & Heron, P. J. (2020). The misuse of colour in science. Nature Communications, 11, 5444 — https://www.nature.com/articles/s41467-020-19160-7
- Crameri, F. Scientific colour maps — https://www.fabiocrameri.ch/colourmaps/
- Borland, D., & Taylor, R. M. (2007). Rainbow Color Map (Still) Considered Harmful — IEEE CG&A — http://dx.doi.org/10.1109/MCG.2007.323435
- ColorBrewer 2.0 (Brewer et al.) — https://colorbrewer2.org/
- Wong, B. (2011). Color blindness — Nature Methods 8, 441 — https://www.nature.com/articles/nmeth.1618
