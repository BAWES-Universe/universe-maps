"""Resolve only bundled C inputs; sibling A/B projects are never consulted."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'source-b-frozen'
FLAT_BUNDLE = ROOT.parents[1] / 'source/frozen-b'
EXPECTED = json.loads((SNAPSHOT / 'SNAPSHOT.json').read_text())['files']


def frozen_b_input(relative):
    """Prefer C's flat B bundle; retain the already-bundled study fallback.

    Existing files with the wrong digest fail closed rather than silently
    selecting another copy. No new raster copy is created by this resolver.
    """
    if relative not in EXPECTED:
        raise ValueError(f'Unpinned B input: {relative}')
    for path in (FLAT_BUNDLE / Path(relative).name, SNAPSHOT / relative):
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != EXPECTED[relative]:
                raise ValueError(f'Frozen B input checksum mismatch: {path}')
            return path
    raise FileNotFoundError(f'Missing bundled B input: {relative}')


def historical_a_comparison():
    """Carry forward archived A evidence only for byte-identical C base/above."""
    evidence = json.loads((ROOT / 'tools/historical-a-comparison.json').read_text())
    for relative, expected in evidence['appliesToFrozenOutputSha256'].items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Historical A proof no longer applies: {relative}')
    return evidence


def review_font(bold=False):
    return str(ROOT / 'tools/fonts' / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'))
