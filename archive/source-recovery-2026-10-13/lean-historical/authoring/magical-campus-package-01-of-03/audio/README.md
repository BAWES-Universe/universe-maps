# Connected campus local sound

This is the existing tested arrival WebAudio controller with one bounded original fire source added and coordinates registered to the new finite gate/campus pair. It is a local-preview integration, not an enabled production audio bridge.

Import `createPreviewAudio` from `arrival-audio.mjs` and load `geometry.json`. Call `start()` directly from the explicit sound-start button, then `setScene('gate'|'campus')` and `setPosition({x,y})` on movement. Coordinates are native character origins; the policy adds16px for feet. `setMuted` applies to all sound. `getCaptureStream()` returns the same post-mute master output, with a zero-valued clock source preserving silent intervals during recording. Mix this stream with the canvas stream, not a post-produced soundtrack.

The gate center path, ordinary campus routes, office, meeting gallery, classroom and event hall are quiet. Only a nearby cascade, fountain or fire plays. At most one location loop plays, with a short transition fade; the gentle gate cue is separately debounced. Call `gateTransition({id,phase:'begin'|'cancel'|'commit'})` from the actual threshold sequence with a unique ID. `setScene` cancels stale gate cues. Call `dispose()` on teardown.

No `silent` Tiled property is created. Proximity conversations, microphones, native rooms, live bots and permissions are untouched. This package does not assign new redistribution terms to the generated assets.

Run `node tests/geometry.mjs` for source-coordinate boundary/mute checks. Actual audible browser playback and map-integrated video must be recorded separately.

## Near-source preview calibration

This version raises only bounded fountain/cascade/fire maximum gains to0.18/0.15/0.18. The global master, gate cue, original asset bytes, quiet zones, mute and source boundaries stay unchanged. The earlier quieter version remains in the parent folder with its evidence. Final output must be measured and heard before a subjective audibility claim. No microphone comparison was sampled, and no claim of guaranteed speech separation is made.
