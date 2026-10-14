#!/usr/bin/env python3
"""Read-only pixel/hash comparison. Registration judgments remain visual."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
expected={
    'r1':'64b14fa317ab4b733136ec2b5e0fcfe8202cdda207f4c50a9dbbdd64dc8f778f',
    'r2':'c90d698d376a4feb2e93d0b44e4c5b4d10c41686e5ce6638f087d3f905f9184a',
}
arrays=[]
for name,h in expected.items():
    path=ROOT/'art/masters'/f'mill-reconstruction-{name}.png'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==h
    im=Image.open(path).convert('RGB');assert im.size==(1536,1024)
    arrays.append(np.asarray(im))
a,b=arrays
changed=int(np.any(a!=b,axis=2).sum());total=int(a.shape[0]*a.shape[1])
print(json.dumps({'sourceHashesMatch':True,'changedPixels':changed,'totalPixels':total,
    'changedPercent':100*changed/total,
    'meanAbsoluteChannelDifference':float(np.abs(a.astype(float)-b).mean()),
    'scope':'Pixel difference only; no geometric or gameplay acceptance.'},indent=2))
