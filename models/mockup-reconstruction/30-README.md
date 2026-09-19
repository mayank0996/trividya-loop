# Trividya physical mockup replica v1

A separate, editable 3D reconstruction of the physical plywood mockup visible in seven supplied photos. It intentionally excludes the tube, guideway, maglev system, healthcare features and other concept overlays.

## Accuracy and scale

**Every dimension is an estimate from uncalibrated photographs.** No measurements or known-size reference were supplied. This is a visual study, not a dimensionally accurate engineering model. Do not fabricate or verify fit from it.

The files use **millimetres** and are modeled at **1:10 scale** for practical Tinkercad import. The estimated full-size envelope is 2050 mm long x 1500 mm wide x 2235 mm high including the top bridge. The model envelope is about 205 x 150 x 223.5 mm. See the JSON and CSV for all labeled estimates and confidence levels.

## Files

- `Trividya-physical-mockup-replica-merged-v1.stl`: one-file import for Tinkercad.
- `Trividya-physical-mockup-replica-grouped-v1.obj` + `.mtl`: named groups and approximate colors.
- `subsystems/*.stl`: separate shell, canopy/window, tail/bridge, rear equipment, service region, and lights/sensor sets.
- `Trividya-physical-mockup-replica-spec-v1.json`: assumptions, exclusions, mesh notes and all estimated dimensions.
- `Trividya-physical-mockup-replica-dimensions-v1.csv`: dimensions in a quick table.
- `previews/*.png`: visually checked reference angles and dimension summary.

## Tinkercad workflow

1. Import the merged STL in millimetres. If it appears too large, set import scale to 100% and verify the envelope is about 205 x 150 x 223.5 mm.
2. For editing, import the subsystem STLs one at a time at the same origin, then group only after changes.
3. OBJ/MTL retains object names/colors better in software that supports grouped OBJ. Tinkercad support varies; STL is the safer path.
4. Intersecting closed parts were kept instead of a heavy global boolean union. This keeps the model practical and less fragile.

## Modeled observations

Plywood side shell, curved/sloped black canopy, small trapezoid window, white panels, broad top bridge on supports, rear equipment housings, fan/vent circles, service doors/openings/handles, side light or sensor pods, top sensor bar, and the hazard-marked lower service panel. Surface text, logos, plywood printing, wiring detail, and unseen internals are omitted.
