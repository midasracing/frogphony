# Kumka — native vector rig and animation

Based on the vector likeness approved by the user. The curves and colours come
from `../kumka-vector/build-vector.py`. No bitmap, mesh, skin or runtime script.

The rig contains a body bone, four leg/arm bones and a shoulder–wrist chain.
The raised arm is split into overlapping vector forearm and hand contours;
the two joints have independently timed rotation. Pupils and highlights share
gaze controls. Full-sized eye shapes are clipped by animated cubic eyelid
apertures; closed eyelids have separate curved creases.

| Timeline | Duration | Behaviour |
| --- | --- | --- |
| Idle | 5 s loop | Quiet breathing and a spontaneous blink |
| Blink | 1.2 s | Fast closure, brief hold, slower reopening |
| LookAround | 3 s | Left/right gaze, small face follow-through, blink on direction change |
| Wave | 2.2 s | Shoulder anticipation, delayed wrist oscillation and settling |
| Success | 2.1 s | Anticipation, takeoff, airborne leg motion, smile and landing compression |

All timelines are 60 fps with cubic easing. All first and last keys return to
the authored resting values. Actions blend in over 100 ms and return to Idle
over 180 ms. Idle is the default. Actions are accepted from Idle; triggers fired
during an action are not queued.

## Runtime contract

- Artboard: `Kumka` (724 × 644, transparent; room above the head for jumping).
- State machine: `KumkaController`.
- View model: `KumkaControls`, default instance `Default`.
- View model triggers: `blink`, `look`, `wave`, `success`.
- These use Rive data binding, not legacy state-machine inputs.
- Ground shadow is native vector geometry and responds to jump height.

With a compatible Rive runtime, bind the default view model instance to the
state machine, then fire its named trigger. Runtime integration in the React
app is a separate step and has not been validated by these CLI captures.

## Files and builds

- `build-rig.py`: reconstructs the rig from approved vector source.
- `scene.rml`: native Rive geometry, skeleton, curves and state machine.
- `rig-manifest.json`: generated animation names, durations and control IDs.
- `render-preview.py`: renders actual view-model-triggered actions with official CLI.
- `render-verification.json`: distinct captured frames per action.
- `kumka-animations.gif` / `.mp4`: 20 fps montage, sampled from 60 fps timelines.
- `kumka.riv`: self-contained native runtime file, also at `public/animations/kumka.riv`.

The preview renderer adds a light background only to its isolated capture
projects; that background is not included in the runtime file.

Build with official Rive CLI 1.8.0:

```sh
python build-rig.py
rive . --verify
rive inspect . --summary
rive . --once
python render-preview.py
```

Verification: native schema check and inspection report zero errors, warnings
or problems. All five timelines close at their rest values. Four actions were
fired through `--data` and sampled across 240 rendered frames. A second Success
trigger after returning to Idle reproduced the same jump frame pixel-for-pixel
(0 of 466,256 pixels differ), confirming the return and retrigger flow.

The `.riv` is a local unsigned runtime build with no scripts. Editable source
is RML plus the Python generator; this is not an editor `.rev` export and has
not been uploaded to the Rive cloud editor. An editor `.rev` export requires
CLI account authentication.
