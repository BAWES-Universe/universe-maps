"""Rebuild the low divider from preserved native stone and front-trim pixels."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
stone = Image.open(ROOT / 'stone-floor-native.png').convert('RGBA')
trim = Image.open(ROOT / 'low-planter.png').convert('RGBA')
output = Image.new('RGBA', (40, 144))
shadow = Image.new('RGBA', output.size)
draw = ImageDraw.Draw(shadow)
draw.rounded_rectangle((5, 14, 38, 140), radius=4, fill=(39, 26, 15, 66))
output.alpha_composite(shadow)
output.alpha_composite(stone.crop((32, 0, 64, 128)), (0, 0))
draw = ImageDraw.Draw(output)
draw.line((0, 0, 31, 0), fill=(255, 238, 191, 240), width=2)
draw.line((0, 0, 0, 126), fill=(255, 233, 180, 180), width=2)
draw.line((30, 3, 30, 126), fill=(101, 79, 47, 185), width=2)
output.alpha_composite(trim.crop((32, 36, 64, 44)), (0, 128))
draw = ImageDraw.Draw(output)
draw.line((3, 127, 28, 127), fill=(160, 129, 77, 255), width=1)
draw.line((8, 8, 8, 119), fill=(70, 118, 105, 160), width=2)
draw.line((23, 8, 23, 119), fill=(70, 118, 105, 160), width=2)
for y in [12, 60, 108]:
    draw.polygon([(15, y), (18, y + 3), (15, y + 6), (12, y + 3)], fill=(77, 130, 111, 170))
output.save(ROOT / 'low-stone-balustrade-native.png')
