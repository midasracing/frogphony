# Kumka — native Rive mascot

Built using official Rive CLI 1.8.0. `scene.rml` contains editable vector shapes and four native timelines, with no scripts or embedded images.

Artboard: `Kumka`. State machine: `KumkaController`.
- `Idle`: 4-second loop, breathing and two blinks.
- `Wave`: 1.5-second arm wave.
- `Success`: 1.25-second hop.
- `Encourage`: 1.5-second head tilt.
Triggers: `wave`, `success`, `encourage`. Each action returns to Idle.

Run `rive . --verify`, `rive inspect . --summary`, `rive . --screenshot --advance=1`, or `rive . --once`.
Runtime asset: `public/animations/kumka.riv`.
The .riv is an unsigned local build. There are no scripts. Verify compatibility with the selected web runtime before integrating.
To obtain a signed runtime export and an editor `.rev`, sign into the official CLI and run `rive . --publish --rev=build/kumka.rev`. Cloud push requires an explicitly selected project/file and overwrites its contents; do not push to an existing file without review.

Visual redraw based on the approved powder-pink toad concept; details differ from the raster concept. Original PNG is retained.
