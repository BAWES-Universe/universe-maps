"""Reproduce the frozen still; writes a new preview and never changes the snapshot."""
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
master = Image.open(ROOT / "source/master-1254.png").convert("RGBA")
assert master.size == (1254, 1254)
preview = master.resize((1024, 1024), Image.Resampling.LANCZOS)
avatar = Image.open(ROOT / "source/greg-scale-reference.png").convert("RGBA").crop((32, 0, 64, 32))
preview.alpha_composite(avatar, (496, 555))
output = ROOT / "rebuild"
output.mkdir(exist_ok=True)
preview.save(output / "preview-1024.png")
