import os
import json
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Categories and name fragments (case-sensitive as files use camel/mixed case)
CATEGORIES = {
    'perceptual': [
        'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'turbo'
    ],
    'sequential': [
        'Blues', 'Greens', 'Reds', 'Purples', 'Oranges', 'Greys', 'Grays',
        'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu',
        'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'bone', 'pink', 'copper', 'gray', 'grey'
    ],
    'diverging': [
        'RdYlBu', 'RdYlGn', 'RdBu', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy',
        'bwr', 'coolwarm', 'seismic', 'Spectral'
    ],
    'qualitative': [
        'Dark2', 'Paired', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'
    ],
    'non-uniform': [
        'jet', 'rainbow', 'hsv', 'hot', 'cool', 'spring', 'summer', 'autumn', 'winter',
        'gist_heat', 'gist_ncar', 'gist_stern', 'brg', 'flag', 'prism', 'nipy_spectral',
        'gnuplot2', 'gnuplot', 'CMRmap', 'afmhot', 'binary', 'gist_earth', 'gist_gray', 'gist_grey',
        'ocean', 'terrain', 'twilight', 'twilight_shifted', 'Wistia'
    ],
}


def base_token(name: str) -> str:
    """Normalize a filename without suffixes like _r or 256."""
    n = name.replace('_r256', '').replace('_r', '').replace('256', '')
    return n


def classify(filename: str) -> str:
    base = os.path.splitext(filename)[0]
    base = base_token(base)
    # Try exact/substring match by priority
    for cat, keys in (
        ('perceptual', CATEGORIES['perceptual']),
        ('non-uniform', CATEGORIES['non-uniform']),
        ('sequential', CATEGORIES['sequential']),
        ('diverging', CATEGORIES['diverging']),
        ('qualitative', CATEGORIES['qualitative']),
    ):
        for k in keys:
            if k in base:
                return cat
    return 'other'


def move_yaml_files():
    src_dir = REPO_ROOT
    dst_root = os.path.join(REPO_ROOT, 'colormaps')
    os.makedirs(dst_root, exist_ok=True)

    # Create subfolders
    for sub in list(CATEGORIES.keys()) + ['other']:
        os.makedirs(os.path.join(dst_root, sub), exist_ok=True)

    moved = []
    for fname in os.listdir(src_dir):
        if not fname.endswith('.yaml'):
            continue
        # Skip if already in colormaps/
        if fname.startswith('colormaps'):
            continue
        category = classify(fname)
        src = os.path.join(src_dir, fname)
        dst = os.path.join(dst_root, category, fname)
        # If destination already exists (script rerun), skip copy/move
        if os.path.exists(dst):
            continue
        shutil.move(src, dst)
        moved.append((fname, category))
    return moved


def build_index_json():
    dst_root = os.path.join(REPO_ROOT, 'colormaps')
    paths = []
    for root, _, files in os.walk(dst_root):
        for f in files:
            if not f.endswith('.yaml'):
                continue
            # Exclude explicit reversed YAMLs; the UI can reverse at runtime
            name_no_ext = os.path.splitext(f)[0]
            if name_no_ext.endswith('_r') or name_no_ext.endswith('_r256'):
                continue
            rel = os.path.relpath(os.path.join(root, f), REPO_ROOT)
            paths.append(rel.replace('\\', '/'))

    paths.sort()
    out_path = os.path.join(REPO_ROOT, 'colormaps_index.json')
    with open(out_path, 'w') as fo:
        json.dump(paths, fo, indent=2)
    return out_path, len(paths)


if __name__ == '__main__':
    moved = move_yaml_files()
    print(f"Moved {len(moved)} YAML files into categorized folders.")
    for fname, cat in moved:
        print(f"  - {fname} -> {cat}")
    out, n = build_index_json()
    print(f"Wrote index with {n} entries to {out}")

