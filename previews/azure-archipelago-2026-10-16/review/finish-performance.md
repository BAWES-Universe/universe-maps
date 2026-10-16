# Final-art performance and water culling

Final TMJ SHA256d5c0e46f269e364538784d2b200545b3ebb4650b0ee70083be4198279968bb62. Engine274114560c5ec95fdf8e51e67986a53069f3cf06, no engine edits. Before artifact38de83948695259e0ddc15e86eb18ea65970bfe5.

Controlled stationary fountain-court spawn comparison: same Chromium,1366×768viewport, camera1/Woka1, one rendering browser (reviewer9222blank), animated water enabled. Each scene was warmed5seconds plus3seconds before15seconds of requestAnimationFrame sampling. Forced dirty after each update avoids misleading idle-render skipping. Alternated before/final/before/final. CDPPerformance counters and profiles retained; no video encoding or screencast during measurement.

| Build | FPS | p95frame ms | Main-thread task seconds | Script seconds |
|---|---:|---:|---:|---:|
| before | 20.39 | 66.7 | 15.09 | 0.406 |
| final | 59.75 | 16.7 | 11.96 | 0.660 |
| before | 31.76 | 50.0 | 15.06 | 0.518 |
| final | 59.96 | 16.8 | 11.42 | 0.623 |

The before samples varied materially; do not quote one percentage speedup or treat this environment as a device guarantee. Both final court samples were near60FPS. Earlier optimization-only matched samples were29.26/28.76before and57.40/59.40after, supporting the direction independently of final artwork.

Final5-second diagnostic samples in six views, sameviewport andforcedredraw, with a short native movement to triggerroofstate:

| View | FPS | Missing partly-visible sea patches |
|---|---:|---:|
| cafe | 37.4 | 0 |
| lounge | 35.5 | 0 |
| garden | 39.4 | 0 |
| gathering | 42.1 | 0 |
| bridge | 56.3 | 0 |
| beach | 40.8 | 0 |

Lounge canopy was confirmed hidden for its sample. These shorter samples are diagnostic, not controlled before/after pairs. Interiors remain heavier than court/bridge, so no whole-map60FPS claim. All six finalviews hadzero missing sea patches; the earlier128pxartifact lost4–12partlyvisible patches in5of6views.

Cause and tradeoff: fullyhidden opaque-covered tiles are removed; transparentcollision/start layers retainall data but opacity0 skips theirdraw.128px animatedsea patches become64pxquadrants within default32pxcullmargin. More small animationinstances slightlyincrease scriptwork, while reducing redundant rendering lowers totaltaskcost. No animationframes/timing were removed; final visualshimmer contrast was reduced afterindependentreview. Nativecamera/Wokascale unchanged. Continuousvideos provevisiblemotion but include captureoverhead and are notbenchmarks. The paintedsea texture/surf remainstatic beneath animatedhighlightlines.
