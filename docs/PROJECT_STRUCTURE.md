# Project structure

The project follows the rule:

> one standalone file = one illustration of one thesis.

Current setup creates only folders and configuration files.

## Folders

- `data/` â€” datasets.
- `figure/` â€” exported figures.
- `chapters/chapter_XX_*` â€” future standalone Python files grouped by handbook chapter.
- `docs/` â€” documentation and notes.
- `notebooks/` â€” optional exploratory notebooks.

## Current restriction

At this stage, do not add:

- data generators;
- plotting scripts;
- reusable plotting modules;
- chapter scripts.

Only `setup.ps1` initializes the project.
