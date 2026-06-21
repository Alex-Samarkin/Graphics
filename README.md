# Scientific Graphics Handbook

Project structure for standalone Python figure files used in a methodological handbook on scientific graphics for medical research.

## Directory structure

```text
data/       Input and prepared datasets
figure/     Generated figure files
chapters/   Chapter-specific standalone figure files
docs/       Notes and documentation
notebooks/  Exploratory notebooks
```

## Setup

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

## Environment

The project uses `uv`.

```powershell
uv sync
```

No data generators or figure scripts are included at the setup stage.
