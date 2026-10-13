#!/usr/bin/env python3
"""NEW restored06 roof reconstruction: a pure, deterministic, bounded map patch.

This is not recovery of, or a hash-equivalence claim about, lost07repair.
Only shared-roof initial visibility and the roof contract retain margin change.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys


def _flatten(layers):
    for layer in layers:
        if layer["type"] == "group":
            yield from _flatten(layer["layers"])
        else:
            yield layer


def patch_roof_map(source):
    """Return a patched copy; never mutate source, collision, or artwork data."""
    result = deepcopy(source)
    contracts = [p for p in result.get("properties", []) if p["name"] == "campusRoofContract"]
    if len(contracts) != 1 or contracts[0].get("type") != "string":
        raise ValueError("Expected exactly one string campusRoofContract")
    contract = json.loads(contracts[0]["value"])
    if contract.get("version") != 1 or contract.get("feetOffsetY") != 16:
        raise ValueError("Expected restored06 native roof contract version 1 and feet offset 16")
    name = contract.get("sharedTranslucentLayer")
    if name != "roof-translucent-shared":
        raise ValueError("Unexpected shared translucent roof layer")
    layers = [layer for layer in _flatten(result["layers"]) if layer["name"] == name]
    if len(layers) != 1 or layers[0]["type"] != "tilelayer":
        raise ValueError("Expected exactly one shared translucent tile layer")
    layers[0]["visible"] = False
    contract["retainMargin"] = 16
    contracts[0]["value"] = json.dumps(contract, ensure_ascii=False, separators=(",", ":"))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", nargs="?", type=Path, help="Omit to write JSON to stdout")
    args = parser.parse_args()
    if args.output and args.input.resolve() == args.output.resolve():
        parser.error("Choose a separate output file; the restored input must remain untouched")
    result = patch_roof_map(json.loads(args.input.read_text()))
    encoded = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        sys.stdout.write(encoded)


if __name__ == "__main__":
    main()
