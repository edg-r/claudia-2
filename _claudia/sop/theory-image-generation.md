---
name: theory-image-generation
description: Explanatory image standard for theory and reference documents
applies_to: all agents creating theory/reference study materials
---

# Theory Image Generation

Theory/reference documents must include one explanatory image for each reading, theory, or framework covered. The image is part of the teaching object, not decoration.

## Required Standard

For every reading, theory, or framework section:

1. Generate or include one explanatory image asset.
2. Place the image in the document near the relevant theory/framework, either on the same page or on an immediately paired visual page when space would otherwise compromise readability.
3. Add a short caption or footnote under the image explaining how the visual maps to the theory:
   - mechanism
   - key assumption
   - strength or limit cue
4. Store project-bound generated images in the workspace asset folder for that document, usually:

```text
[Course Folder]/Study Guides/assets/<project_slug>/
```

## Approved Visual Style

Use the approved MacIntyre prototype standard as the default visual family for theory/reference PDFs: explanatory academic images that combine compact diagrams with concrete political-economy scenes.

Preferred formats:

- graph-plus-vignettes, where the graph teaches the causal shape and small scenes anchor cases
- case lanes showing different countries, institutions, or policy paths
- compact institutional diagrams with actors, rules, and decision points
- concrete political-economy scenes tied to course cases
- classroom textbook visual explainers with clean spacing and obvious mechanism cues

## Text Density

Keep image text low density. Use 0-4 short labels whenever possible. Labels should name the mechanism or contrast, not restate the whole theory.

## Avoid

Do not use:

- abstract images with giant arrows
- vague metaphor art
- text-heavy infographics
- decorative gradients, orbs, or purely atmospheric backgrounds
- unsupported citations or invented source claims inside images
- flags as decoration when they are not doing explanatory work
- stock-photo moodiness or blurred cinematic scenes
- images that look polished but do not teach the theory

## Prototype Before Batch

When establishing a new image family or visual style for a document, generate one prototype first and return it for Edgar critique before producing the remaining batch.

After Edgar approves the prototype style, apply that style consistently across the remaining reading/theory/framework images.

## Tooling and File Handling

Use the built-in image generation path by default. Use a CLI fallback only if Edgar explicitly chooses that route or the built-in tool is unavailable and Claudia approves fallback.

Generated images created outside the workspace must be copied into the relevant project asset folder before the deliverable is treated as complete. The document build script should reference the workspace copy, not a transient tool output path.
