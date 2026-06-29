# Slides and Posters V2 Roadmap

## Goal
Upgrade the current HTML-first conference deliverables into a stronger congress production system: better rule import, better visual design, richer PPTX, real templates, better QA, and safer portal submission.

## Priority 1: Refactor and Contracts
- Split `article_machine/deliverables.py` into focused modules: `conference.py`, `storyboard.py`, `layout.py`, `qa.py`, `export.py`, and `submission.py`.
- Add explicit schema validation for `conference.yaml`, `storyboard.yaml`, `theme.yaml`, and `qa_report.json`.
- Version exports instead of appending duplicate manifest entries for repeated export runs.
- Add tests for deck, poster, abstract, handout, and submission-pack contracts.

## Priority 2: Requirement Import
- Improve congress rule import from URL, PDF, screenshot/OCR, markdown, and pasted text.
- Extract dimensions, orientation, duration, slide count, abstract word count, file types, logo requirements, deadline, portal URL, and confidence score.
- Add a `requirements_confidence` field and block strict export when required rules are ambiguous.

## Priority 3: Visual Layout Engine
- Add real visual templates for 3-min, 5-min, 10-min, 15-min, seminar, thesis defense, A0 portrait, A0 landscape, 36x48 portrait, and 48x36 landscape.
- Support reusable themes with palette, typography, institutional branding, author blocks, affiliations, logos, QR code, and references.
- Add automatic density reduction for overcrowded slides/poster blocks.

## Priority 4: Rich Exports
- Upgrade PPTX export with richer editable text boxes, speaker notes, images, charts, poster blocks, and slide duplication for build steps.
- Keep HTML as canonical source.
- Keep PDF as print/presentation output.
- Keep PPTX as editable fallback.

## Priority 5: Figures and AI Visuals
- Connect data figures from R/Python outputs under `analysis/`.
- Route technical diagrams to `scientific-schematics`.
- Route title/hero images to GPT Image or fallback HTML/CSS.
- Enforce asset provenance and `source_claim_ids`.

## Priority 6: Playwright QA and Submission
- Add per-slide screenshots and per-poster-block screenshots.
- Add contrast, font, overflow, margin, image resolution, page size, and visual regression checks.
- Build portal-specific dry-run adapters.
- Require explicit human confirmation for final submission.

## Priority 7: Saved Congress Profiles
- Save imported congress rules as reusable local profiles.
- Allow commands like `article-machine congress use-profile <project_dir> --profile <name> --slug <slug>`.
- Track profile provenance and last verification date.
