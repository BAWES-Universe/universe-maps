"""Light v3 room materials, sampled from full-resolution original masters.

This module has no map/physics side effects.  room_shell() returns same-size
RGBA floor, bases, and front canvases; light_assets() returns exact-size prop
replacements.  Run this file to regenerate light-*.png and the contact proof.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / 'art-source'
PROPOSAL = ROOT / 'interior-proposal-light' / 'art-source'
ASSETS = ROOT / 'assets'
NORTH = 112
SIDE = 24  # Painted width.  The existing collision width remains 32.
SOUTH = 64
DOOR = 128

# Full-resolution, hand-inspected object boxes in the genuine-alpha original.
FURNITURE_BOXES = {
    'desk': (45, 143, 488, 413),
    'teacher': (45, 143, 488, 413),
    'chair_n': (683, 157, 943, 443),
    'chair_s': (1157, 113, 1403, 459),
    'reception': (5, 548, 573, 936),
    'meeting_table': (600, 602, 1028, 901),
    'rug': (1048, 563, 1535, 908),
}
EXPECTED_SIZES = {
    'desk': (63, 44), 'teacher': (52, 48), 'chair_n': (28, 32),
    'chair_s': (26, 37), 'reception': (143, 104),
    'meeting_table': (121, 76), 'rug': (224, 127),
}


def _downsample(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """One alpha-correct downsample; reject accidental source inflation."""
    if size[0] > image.width or size[1] > image.height:
        raise ValueError(f'No upscale: source {image.size}, requested {size}')
    if size == image.size:
        return image.copy().convert('RGBA')
    return image.convert('RGBa').resize(size, Image.Resampling.LANCZOS).convert('RGBA')


@lru_cache(maxsize=1)
def _masters() -> dict[str, Image.Image]:
    # The cleared v1 derivative is still the original 1536x1024 resolution.
    # It is the same wall master used in the approved light-room proposal.
    return {
        'wall': Image.open(V1 / 'accepted-v1-interiors-empty-floor.png').convert('RGBA'),
        'occupied': Image.open(V1 / 'accepted-v1-interiors-source.png').convert('RGBA'),
        'furniture': Image.open(PROPOSAL / 'furniture-original.png').convert('RGBA'),
        'sandstone': Image.open(PROPOSAL / 'sandstone-floor-original.png').convert('RGBA'),
    }


def _repeat(texture: Image.Image, width: int, height: int) -> Image.Image:
    result = Image.new('RGBA', (width, height))
    for y in range(0, height, texture.height):
        for x in range(0, width, texture.width):
            # alpha_composite clips at the destination edge; no texture scaling.
            result.alpha_composite(texture, (x, y))
    return result


@lru_cache(maxsize=1)
def sandstone_tile() -> Image.Image:
    """A 640px tile, reduced once from the 1254px sandstone source."""
    return _downsample(_masters()['sandstone'], (640, 640))


def _shelf_run(width: int, right: bool = False) -> Image.Image:
    """Fit complete individual bookcase bays, never inflate a whole wall."""
    source = _masters()['wall']
    boxes = ([(559, 51, 625, 210), (625, 51, 690, 210), (690, 51, 753, 210)]
             if right else
             [(164, 51, 230, 210), (230, 51, 296, 210), (296, 51, 360, 210)])
    pieces, source_width = [], 0
    while source_width < width:
        piece = source.crop(boxes[len(pieces) % len(boxes)])
        pieces.append(piece)
        source_width += piece.width
    run = Image.new('RGBA', (source_width, 159))
    x = 0
    for piece in pieces:
        run.alpha_composite(piece, (x, 0))
        x += piece.width
    return _downsample(run, (width, 106))


def north_wall(width: int) -> Image.Image:
    """112px wall: two end bays, individual bookcase runs, central teal arch."""
    if width < 448:
        raise ValueError('The pale architectural shell requires width >= 448')
    source = _masters()['wall']
    result = Image.new('RGBA', (width, NORTH))
    end, center = 74, 160
    left_width = (width - 2 * end - center) // 2
    right_width = width - 2 * end - center - left_width
    result.alpha_composite(_downsample(source.crop((72, 51, 164, 210)), (end, 106)), (0, 6))
    result.alpha_composite(_shelf_run(left_width), (end, 6))
    result.alpha_composite(_downsample(source.crop((360, 43, 559, 210)), (center, 112)), (end + left_width, 0))
    result.alpha_composite(_shelf_run(right_width, right=True), (end + left_width + center, 6))
    result.alpha_composite(_downsample(source.crop((753, 51, 829, 210)), (end, 106)), (width - end, 6))
    return result


def wall_strip(width: int, height: int = SOUTH) -> Image.Image:
    """Warm pale parapet for south walls and optional interior partitions.

    The native 17px cap stays intact. Native masonry courses fill the face;
    widening adds original stone segments instead of stretching a bitmap.
    """
    if width <= 0 or height <= 0:
        raise ValueError('Wall dimensions must be positive')
    source = _masters()['occupied']
    cap = source.crop((75, 483, 348, 500))
    face = source.crop((75, 500, 348, 530))
    result = Image.new('RGBA', (width, height))
    cap_height = min(17, height)
    result.alpha_composite(_repeat(cap, width, cap_height), (0, 0))
    if height > cap_height:
        result.alpha_composite(_repeat(face, width, height - cap_height), (0, cap_height))
    return result


def side_wall(height: int) -> Image.Image:
    """24px pale side wall, downsampled once and extended in native segments."""
    original = _masters()['occupied'].crop((75, 483, 348, 532))
    segment = _downsample(original.transpose(Image.Transpose.ROTATE_90), (SIDE, 273))
    return _repeat(segment, SIDE, height)


@lru_cache(maxsize=1)
def lantern_column() -> Image.Image:
    """An actual v1 lantern pier, with surrounding floor explicitly excluded.

    A source-space contour isolates the depicted column and lantern, rather
    than promoting the rectangular crop (which contains floor) to foreground.
    Original alpha is retained inside the contour. No new artwork is painted.
    """
    box = (344, 438, 403, 540)
    source = _masters()['occupied'].crop(box)
    mask = Image.new('L', source.size)
    d = ImageDraw.Draw(mask)
    # Hand-inspected silhouette in original source pixels.
    d.polygon([(29, 0), (35, 3), (37, 11), (43, 18), (45, 27),
               (43, 37), (40, 44), (45, 45), (47, 51), (45, 57),
               (15, 57), (14, 49), (19, 44), (15, 35), (14, 24),
               (19, 14), (25, 10), (26, 3)], fill=255)
    d.polygon([(9, 37), (48, 37), (51, 48), (51, 96), (47, 101),
               (9, 101), (5, 96), (5, 53)], fill=255)
    source.putalpha(ImageChops.multiply(source.getchannel('A'), mask))
    return _downsample(source, (42, 74))


def room_shell(width: int, height: int) -> dict[str, Image.Image]:
    """Return transparent RGBA layers exactly (width, height).

    Existing geometry remains the caller's responsibility and must not change:
    north=112, side collision=32, south=64, centered clear doorway=128.
    The threshold is on floor only; no wall or pier crosses into that opening.
    """
    width, height = int(width), int(height)
    if width < 448 or height < 256:
        raise ValueError('Room must be at least 448 x 256 pixels')
    result = {name: Image.new('RGBA', (width, height)) for name in ('floor', 'bases', 'front')}
    floor, bases, front = (result[name] for name in ('floor', 'bases', 'front'))
    floor.alpha_composite(_repeat(sandstone_tile(), width - 2 * SIDE, height - NORTH), (SIDE, NORTH))
    floor.alpha_composite(north_wall(width), (0, 0))
    # A narrow original-color inlay frames only the two side edges. There is no
    # horizontal stripe across the floor opening and no foreground threshold.
    draw = ImageDraw.Draw(floor)
    for x in (SIDE + 3, width - SIDE - 4):
        draw.line((x, NORTH, x, height - 1), fill=(147, 169, 146, 255), width=2)
    side = side_wall(height - NORTH)
    front.alpha_composite(side, (0, NORTH))
    front.alpha_composite(side.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (width - SIDE, NORTH))
    door_left = (width - DOOR) // 2
    door_right = door_left + DOOR
    for x, span in ((0, door_left), (door_right, width - door_right)):
        wall = wall_strip(span)
        bases.alpha_composite(wall.crop((0, 40, span, 64)), (x, height - 24))
        front.alpha_composite(wall.crop((0, 0, span, 40)), (x, height - 64))
    pier = lantern_column()
    for x in (0, door_left - pier.width, door_right, width - pier.width):
        cut = pier.height - 24
        bases.alpha_composite(pier.crop((0, cut, pier.width, pier.height)), (x, height - 24))
        front.alpha_composite(pier.crop((0, 0, pier.width, cut)), (x, height - pier.height))
    # Paint and collision must agree at the complete existing clear opening.
    doorway = (door_left, height - SOUTH, door_right, height)
    assert front.crop(doorway).getchannel('A').getbbox() is None
    assert bases.crop(doorway).getchannel('A').getbbox() is None
    assert floor.crop(doorway).getchannel('A').getextrema()[0] == 255
    return result


def light_assets() -> dict[str, Image.Image]:
    """Exact-canvas replacements from one downsample of genuine-alpha source."""
    sheet = _masters()['furniture']
    result = {}
    for name, box in FURNITURE_BOXES.items():
        with Image.open(ASSETS / f'{name}.png') as existing:
            size = existing.size
        if size != EXPECTED_SIZES[name]:
            raise ValueError(f'Unexpected {name} canvas {size}; expected {EXPECTED_SIZES[name]}')
        crop = sheet.crop(box)
        # Threshold identifies the object bounds only. Generated alpha is never
        # thresholded, flood-filled, recolored, or replaced in the final sprite.
        bounds = crop.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
        if bounds is None:
            raise ValueError(f'No visible object in {name} source crop')
        result[name] = _downsample(crop.crop(bounds), size)
    return result


def _proof(overrides: dict[str, Image.Image]) -> Image.Image:
    """Native-size HQ shell plus correctly scaled furniture contact proof."""
    width, height = 960, 832
    layers = room_shell(width, height)
    # Useful composition only; not a replacement map or new collision layout.
    placements = [('desk', 80, 176), ('chair_n', 98, 232),
                  ('desk', 256, 176), ('chair_n', 274, 232),
                  ('teacher', 448, 174), ('chair_n', 460, 234),
                  ('meeting_table', 688, 216),
                  ('chair_s', 699, 171), ('chair_s', 758, 171),
                  ('chair_n', 699, 297), ('chair_n', 758, 297),
                  ('reception', 112, 608), ('chair_s', 168, 559)]
    layers['floor'].alpha_composite(overrides['rug'], (637, 188))
    layers['floor'].alpha_composite(overrides['rug'], (630, 552))
    for name, x, y in [('couch_s', 688, 524), ('couch_e', 616, 576),
                       ('couch_w', 822, 576), ('coffee', 706, 603),
                       ('plant', 54, 376), ('plant', 849, 388),
                       ('plant', 64, 714), ('plant', 848, 714)]:
        placements.append((name, x, y))
    for name, x, y in placements:
        sprite = overrides.get(name)
        if sprite is None:
            sprite = Image.open(ASSETS / f'{name}.png').convert('RGBA')
        cut = max(0, sprite.height - 32)
        layers['bases'].alpha_composite(sprite.crop((0, cut, sprite.width, sprite.height)), (x, y + cut))
        layers['front'].alpha_composite(sprite.crop((0, 0, sprite.width, cut)), (x, y))
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    proof = Image.new('RGBA', (1280, 924), (242, 239, 227, 255))
    d = ImageDraw.Draw(proof)
    d.text((24, 16), 'LIGHT ROOM MATERIALS · 960 × 832 native shell · source-segment construction', font=font, fill=(52, 83, 72))
    room = layers['floor'].copy()
    room.alpha_composite(layers['bases'])
    greg_path = ROOT / 'qa' / 'greg.png'
    if greg_path.exists():
        greg = Image.open(greg_path).convert('RGBA')
        room.alpha_composite(greg.crop((32, 0, 64, 32)), (464, 790))
        room.alpha_composite(greg.crop((32, 32, 64, 64)), (348, 254))
    room.alpha_composite(layers['front'])
    proof.alpha_composite(room, (24, 48))
    d.text((24, 895), 'Pale sandstone · warm original masonry · teal + brass accents · 128px clear doorway', font=small, fill=(52, 83, 72))
    d.text((1010, 48), 'Exact current sprite canvases', font=small, fill=(52, 83, 72))
    y = 88
    for name, sprite in overrides.items():
        d.text((1010, y), f'{name}  {sprite.width}×{sprite.height}', font=small, fill=(52, 83, 72))
        d.rounded_rectangle((1008, y + 20, 1260, y + 30 + sprite.height), radius=4,
                            fill=(232, 231, 216, 255), outline=(213, 214, 194, 255))
        proof.alpha_composite(sprite, (1024, y + 25))
        y += sprite.height + 54
    return proof


def main() -> None:
    overrides = light_assets()
    for name, sprite in overrides.items():
        sprite.save(ASSETS / f'light-{name}.png')
    for width, height in ((704, 672), (704, 608), (928, 608), (960, 832)):
        layers = room_shell(width, height)
        for name, image in layers.items():
            image.save(ASSETS / f'light-shell-{width}x{height}-{name}.png')
    side_wall(304).save(ASSETS / 'light-side-wall.png')
    wall_strip(395).save(ASSETS / 'light-wall-strip.png')
    lantern_column().save(ASSETS / 'light-lantern-column.png')
    _proof(overrides).save(ASSETS / 'light-proof.png')
    print('Generated exact-size light furniture and verified 4 transparent room shells.')


if __name__ == '__main__':
    main()
