"""Pack native Tiled effects without repeated frame tiles or cross-page animation IDs."""
from pathlib import Path
from PIL import Image
import math


def pack_effect(effect, root, output, first_gid, world_size, tile=32, page_cells=1024):
    frames = [Image.open(root / path).convert('RGBA') for path in effect['frames']]
    if not frames or len({frame.size for frame in frames}) != 1:
        raise ValueError('Effect frames must have one consistent native size')
    ox, oy = effect['origin']
    if not isinstance(ox, int) or not isinstance(oy, int):
        raise ValueError('Effect origins must be integer native pixels')
    width, height = frames[0].size
    if ox < 0 or oy < 0 or ox + width > world_size[0] or oy + height > world_size[1]:
        raise ValueError('Effect leaves the finite world')
    durations = effect['durations'] if 'durations' in effect else [effect['duration']] * len(frames)
    if len(durations) != len(frames) or any(not isinstance(d, int) or d <= 0 for d in durations):
        raise ValueError('Every frame needs a positive duration')
    x0, y0 = ox // tile * tile, oy // tile * tile
    padded_size = (math.ceil((ox - x0 + width) / tile) * tile,
                   math.ceil((oy - y0 + height) / tile) * tile)
    padded = []
    for frame in frames:
        canvas = Image.new('RGBA', padded_size)
        canvas.paste(frame, (ox - x0, oy - y0))
        padded.append(canvas)

    pages, cells, audit = [], {}, {'effect': effect['name'], 'layer': effect.get('layer', 'below'),
                                 'sourceFrames': len(frames), 'animatedCells': 0,
                                 'staticCells': 0, 'varyingCells': 0, 'storedTiles': 0,
                                 'uniqueAnimations': 0, 'nativeFrameRoundTrip': True}
    parts, image_ids, sequences, metadata = [], {}, {}, []
    page_first = first_gid

    def add_image(blob):
        if blob not in image_ids:
            image_ids[blob] = len(parts)
            parts.append(Image.frombytes('RGBA', (tile, tile), blob))
        return image_ids[blob]

    def flush():
        nonlocal parts, image_ids, sequences, metadata, page_first
        if not parts:
            return
        columns = min(32, len(parts))
        atlas = Image.new('RGBA', (columns * tile, math.ceil(len(parts) / columns) * tile))
        for i, part in enumerate(parts):
            atlas.paste(part, ((i % columns) * tile, (i // columns) * tile))
        name = f"{effect['name']}-p{len(pages)}"
        atlas.save(output / (name + '.png'))
        tileset = {'firstgid': page_first, 'name': name, 'image': name + '.png',
                   'imagewidth': atlas.width, 'imageheight': atlas.height,
                   'tilewidth': tile, 'tileheight': tile, 'margin': 0, 'spacing': 0,
                   'columns': columns, 'tilecount': len(parts)}
        if metadata:
            tileset['tiles'] = metadata
        pages.append(tileset)
        audit['storedTiles'] += len(parts)
        audit['uniqueAnimations'] += len(metadata)
        page_first += len(parts)
        parts, image_ids, sequences, metadata = [], {}, {}, []

    for y in range(0, padded_size[1], tile):
        for x in range(0, padded_size[0], tile):
            images = [frame.crop((x, y, x + tile, y + tile)) for frame in padded]
            if all(image.getchannel('A').getbbox() is None for image in images):
                continue
            blobs = tuple(image.tobytes() for image in images)
            cell = ((y0 + y) // tile) * (world_size[0] // tile) + (x0 + x) // tile
            if len(set(blobs)) == 1:
                if blobs[0] not in image_ids and len(parts) == page_cells:
                    flush()
                cells[cell] = page_first + add_image(blobs[0])
                audit['staticCells'] += 1
                continue
            sequence = tuple(zip(blobs, durations))
            if sequence not in sequences:
                if len(set(blobs)) + 1 > page_cells:
                    raise ValueError('One animation exceeds an atlas page')
                needed = len(set(blobs) - image_ids.keys()) + 1
                if len(parts) + needed > page_cells:
                    flush()
                ids = [add_image(blob) for blob in blobs]
                # A distinct owner tile avoids sharing metadata between different
                # animations that happen to start with identical pixels.
                owner = len(parts)
                parts.append(images[0])
                metadata.append({'id': owner, 'animation': [
                    {'tileid': frame_id, 'duration': duration}
                    for frame_id, duration in zip(ids, durations)]})
                sequences[sequence] = owner
                assert all(parts[frame_id].tobytes() == blob for frame_id, blob in zip(ids, blobs))
            cells[cell] = page_first + sequences[sequence]
            audit['animatedCells'] += 1
            audit['varyingCells'] += 1
    flush()
    audit['atlasPages'] = len(pages)
    audit['oldNaiveFrameTiles'] = (audit['animatedCells'] + audit['staticCells']) * len(frames)
    return pages, cells, page_first, audit
