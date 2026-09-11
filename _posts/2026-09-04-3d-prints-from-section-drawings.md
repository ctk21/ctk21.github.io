---
layout: post
title: Making 3D prints from section drawings
date: 2026-09-04
description: Creating a physical model from engineering section drawings.
tags:
  - cad
  - 3d-printing
  - engineering
---

Section drawings are often the clearest description of an assembly's internal shape. They can also be a useful starting point for a small physical model: trace the visible profile, give it a controlled depth, and print a test piece before committing to a larger build.

## Start with the section, not the object

Choose a section that shows the features the model needs to communicate. Record the drawing scale, establish a single unit system, and identify which edges describe material rather than hidden detail. For most printers, working in millimetres keeps the CAD model, slicer, and measurements aligned.

Before modelling, make a short list of decisions:

- which dimensions must stay true to the drawing;
- which small details can be simplified;
- the extrusion depth of the model; and
- the orientation that gives the print stable support.

> A section drawing is a view of an object, not always a complete manufacturing specification. Treat uncertain dimensions as assumptions and label them in the model.

## Trace a printable profile

Trace the section as a closed two-dimensional outline. Keep the first version deliberately simple: large steps, holes, and wall boundaries are more useful than decorative edges. If the drawing uses a scale, convert every selected measurement before entering it into CAD.

The following small [OpenSCAD](https://openscad.org/documentation.html) example turns a traced profile into a solid. The coordinates are illustrative; replace them with dimensions taken from the drawing.

```scad
profile = [
  [0, 0], [72, 0], [72, 8], [48, 8],
  [48, 28], [30, 28], [30, 45], [0, 45]
];

linear_extrude(height = 12)
  polygon(points = profile);
```

`linear_extrude` makes the relationship between the drawing and the model explicit: the section becomes the printed face, while the extrusion sets the model depth.

| Drawing input | Modelling decision |
| --- | --- |
| Overall width and height | Use as the profile's primary dimensions. |
| Thin wall or slot | Widen only when it would fall below the printer's reliable feature size. |
| Repeated section | Model one representative portion unless repetition is important to the explanation. |
| Unknown depth | Choose a clearly stated extrusion depth for the first test. |

## Test the part early

Export the model to a slicer and inspect the layer preview before printing. Check that narrow walls survive, unsupported overhangs are acceptable, and the chosen orientation makes the section readable. A short, low-infill test print is usually enough to reveal scale mistakes or features that need to be simplified.

When the test is useful, revise the profile rather than patching the mesh. Keeping the source as ordinary CAD makes later changes to `wall_thickness`, depth, or scale straightforward and keeps the printed model tied to the original drawing.
