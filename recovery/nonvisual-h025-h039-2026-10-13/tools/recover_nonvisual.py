#!/usr/bin/env python3
"""Re-emit only art-independent source data from pinned retained Python source.

No raster artwork, TMJ, WAM, placeholder map or acceptance certificate is made.
The H025 loop omits pixel-loading/compositing statements; its two mask sizes use
the exact 1248x1248 crop dimensions asserted by the retained builder.
"""
from pathlib import Path
import ast
import copy
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / 'generated'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs():
    for item in json.loads((ROOT / 'retained-inputs.json').read_text())['files']:
        assert sha(ROOT / item['path']) == item['sha256'], item['path']


def run_nodes(nodes, filename, env):
    tree = ast.fix_missing_locations(ast.Module(body=copy.deepcopy(nodes), type_ignores=[]))
    exec(compile(tree, str(filename), 'exec'), env)


def setup(mapid):
    output = OUT / mapid
    for folder in ['source', 'validation', 'tools', 'map32' if mapid == 'H025' else 'runtime']:
        (output / folder).mkdir(parents=True, exist_ok=True)
    source = ROOT / 'retained' / mapid
    shutil.copyfile(source / 'source/controller.js', output / 'source/controller.js')
    return source, output


def recover_h025():
    source, output = setup('H025')
    for name in ['author-layout.py', 'author-floor.py']:
        # Execute the unmodified generator, with its destination rooted in the
        # new output tree. The retained input file is never changed.
        exec(compile((source / 'tools' / name).read_text(), str(source / 'tools' / name), 'exec'),
             {'__file__': str(output / 'tools' / name), '__name__': '__main__'})
    filename = source / 'tools/build.py'
    nodes = ast.parse(filename.read_text()).body
    assert isinstance(nodes[17], ast.For) and nodes[17].lineno == 9
    loop = copy.deepcopy(nodes[17])
    # All retained geometric/control statements are unchanged. Art pixels are
    # not read; mask dimensions follow the existing 1248-square image crop.
    loop.body = [copy.deepcopy(loop.body[i]) for i in [0, *range(5, 26), 32]]
    for statement in loop.body:
        if isinstance(statement, ast.Assign) and ast.unparse(statement.targets[0]) in ['m', 'hard']:
            assert ast.unparse(statement.value.args[1]) == 'im.size'
            statement.value.args[1] = ast.Tuple(elts=[ast.Constant(1248), ast.Constant(1248)], ctx=ast.Load())
    selected = [*nodes[:7], nodes[8], *nodes[12:17], loop, *nodes[18:22], nodes[48]]
    env = {'__file__': str(output / 'tools/build.py'), '__name__': '__main__'}
    run_nodes(selected, filename, env)
    return env


def recover_h039():
    source, output = setup('H039')
    shutil.copyfile(source / 'source/design.json', output / 'source/design.json')
    filename = source / 'tools/build.py'
    nodes = ast.parse(filename.read_text()).body
    assert nodes[21].lineno == 21 and nodes[94].lineno == 88
    selected = [*nodes[:7], nodes[11], *nodes[21:28], nodes[86], nodes[87], nodes[94]]
    env = {'__file__': str(output / 'tools/build.py'), '__name__': '__main__'}
    run_nodes(selected, filename, env)
    script = output / 'runtime/experience.js'
    expected = '96cc654f6a1cbfb83d4c0e14269e11f428912b5029b49f022ab067cf3d15ddf3'
    assert sha(script) == expected, 'H039 final historical interaction hash mismatch'
    return env


def main():
    verify_inputs()
    recover_h025()
    recover_h039()
    rows = []
    for p in sorted(OUT.rglob('*')):
        if p.is_file() and 'validation' not in p.parts and p.name != 'DERIVATION.json':
            rows.append({'path': str(p.relative_to(OUT)), 'bytes': p.stat().st_size, 'sha256': sha(p)})
    report = {'scope': 'New art-independent source derivation, not a recovered complete map or visual/live acceptance.',
              'artFilesCreated': 0, 'tmjFilesCreated': 0, 'wamFilesCreated': 0,
              'historicalHashMatches': {'H039/runtime/experience.js': '96cc654f6a1cbfb83d4c0e14269e11f428912b5029b49f022ab067cf3d15ddf3'},
              'unverifiedHistoricalIdentity': 'All other derived outputs have current checksums only; no original per-file checksum was retained.',
              'files': rows}
    (OUT / 'DERIVATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
