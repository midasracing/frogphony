# Kumka — vector likeness study

Hand-authored Bézier reconstruction of the approved pink toad. This is the
artwork review stage before final rigging and animation.

- `kumka-vector.svg`: 23 named vector elements, transparent background, editable cubic curves and gradients.
- `scene.rml`: the same geometry as native Rive shapes and paths.
- `build-vector.py`: generates both formats from one source of truth.
- `kumka-comparison.png`: approved original on the left, native Rive render on the right.
- `kumka-vector.riv`: static native Rive study; not an editable `.rev` project.

Features are separate: body, belly, both hind legs, raised arm, both front arms,
creases, four spots, eye whites, pupils, glints, nostrils, smile and smile corner.
Small differences in contour and shading remain for likeness review.
No bitmap, image mesh, skinning or runtime script is used. This is a new study;
it does not replace the deployed mascot or ship the rejected mesh animation.

Verified with official Rive CLI 1.8.0: 0 errors, 0 warnings; 23 Shapes,
23 PointsPaths, 148 cubic vertices, 0 Images, 0 Meshes, 0 ImageAssets.

Build: `python build-vector.py`, then `rive . --verify`,
`rive inspect . --summary`, and `rive . --once`.

Animation work follows likeness review: joint pivots and bone hierarchy,
eyelid paths and clipping, eye tracking, mouth poses, then timed actions with
anticipation, follow-through, easing and state-machine transitions. These are
not implemented by this static study.
