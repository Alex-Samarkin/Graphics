# setup.ps1
# Initial project setup for the scientific graphics handbook.
# Windows 11 + VS Code + uv.
#
# Run from the empty project directory:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#   .\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Scientific Graphics Project Setup ===" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------------------
# 1. Check location
# ----------------------------------------------------------------------
$ProjectRoot = Get-Location
Write-Host "Project root: $ProjectRoot"

# ----------------------------------------------------------------------
# 2. Check uv
# ----------------------------------------------------------------------
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "uv was not found in PATH." -ForegroundColor Yellow
    Write-Host "Install uv first, then run this script again:"
    Write-Host "  powershell -ExecutionPolicy ByPass -c ""irm https://astral.sh/uv/install.ps1 | iex"""
    exit 1
}

Write-Host "uv found:" -ForegroundColor Green
uv --version

# ----------------------------------------------------------------------
# 3. Create directory structure
# ----------------------------------------------------------------------
$Dirs = @(
    "data",
    "data\raw",
    "data\processed",
    "figure",
    "chapters",
    "chapters\chapter_01_general_principles",
    "chapters\chapter_02_environment",
    "chapters\chapter_03_distributions",
    "chapters\chapter_04_category_comparison",
    "chapters\chapter_05_relationships_regression",
    "chapters\chapter_06_color_palettes",
    "chapters\chapter_07_medical_special_plots",
    "chapters\chapter_08_axes_legends_captions",
    "chapters\chapter_09_composite_export",
    "chapters\chapter_10_reproducibility",
    "chapters\chapter_11_formats",
    "chapters\chapter_12_checklists_templates",
    "docs",
    "notebooks"
)

foreach ($Dir in $Dirs) {
    if (-not (Test-Path $Dir)) {
        New-Item -ItemType Directory -Path $Dir | Out-Null
        Write-Host "Created: $Dir"
    }
    else {
        Write-Host "Exists:  $Dir"
    }
}

# Keep empty folders visible in Git
foreach ($Dir in $Dirs) {
    $KeepFile = Join-Path $Dir ".gitkeep"
    if (-not (Test-Path $KeepFile)) {
        New-Item -ItemType File -Path $KeepFile | Out-Null
    }
}

# ----------------------------------------------------------------------
# 4. Initialize uv project files only if absent
# ----------------------------------------------------------------------
if (-not (Test-Path "pyproject.toml")) {
@'
[project]
name = "scientific-graphics-handbook"
version = "0.1.0"
description = "Standalone Python figures for a methodological handbook on scientific graphics in medical research."
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "numpy",
    "pandas",
    "scipy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "lifelines",
    "statannotations",
    "jupyter",
    "ipykernel",
]

[tool.uv]
package = false
'@ | Set-Content -Path "pyproject.toml" -Encoding UTF8
    Write-Host "Created: pyproject.toml"
}
else {
    Write-Host "Exists:  pyproject.toml"
}

if (-not (Test-Path ".python-version")) {
    "3.12" | Set-Content -Path ".python-version" -Encoding UTF8
    Write-Host "Created: .python-version"
}
else {
    Write-Host "Exists:  .python-version"
}

# ----------------------------------------------------------------------
# 5. Create GitHub-oriented service files
# ----------------------------------------------------------------------
if (-not (Test-Path ".gitignore")) {
@'
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python

# Virtual environments
.venv/
venv/
env/

# uv
uv.lock

# Jupyter
.ipynb_checkpoints/

# VS Code local settings
.vscode/settings.json

# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
*.log

# Generated figures can be large.
# Remove the next line if you want to version generated figures.
figure/*
!figure/.gitkeep

# Data can contain local or sensitive files.
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep
'@ | Set-Content -Path ".gitignore" -Encoding UTF8
    Write-Host "Created: .gitignore"
}
else {
    Write-Host "Exists:  .gitignore"
}

if (-not (Test-Path "README.md")) {
@'
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
'@ | Set-Content -Path "README.md" -Encoding UTF8
    Write-Host "Created: README.md"
}
else {
    Write-Host "Exists:  README.md"
}

if (-not (Test-Path "docs\PROJECT_STRUCTURE.md")) {
@'
# Project structure

The project follows the rule:

> one standalone file = one illustration of one thesis.

Current setup creates only folders and configuration files.

## Folders

- `data/` — datasets.
- `figure/` — exported figures.
- `chapters/chapter_XX_*` — future standalone Python files grouped by handbook chapter.
- `docs/` — documentation and notes.
- `notebooks/` — optional exploratory notebooks.

## Current restriction

At this stage, do not add:

- data generators;
- plotting scripts;
- reusable plotting modules;
- chapter scripts.

Only `setup.ps1` initializes the project.
'@ | Set-Content -Path "docs\PROJECT_STRUCTURE.md" -Encoding UTF8
    Write-Host "Created: docs\PROJECT_STRUCTURE.md"
}
else {
    Write-Host "Exists:  docs\PROJECT_STRUCTURE.md"
}

# ----------------------------------------------------------------------
# 6. Create VS Code recommendations, but no local settings
# ----------------------------------------------------------------------
if (-not (Test-Path ".vscode")) {
    New-Item -ItemType Directory -Path ".vscode" | Out-Null
}

if (-not (Test-Path ".vscode\extensions.json")) {
@'
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "ms-toolsai.jupyter"
  ]
}
'@ | Set-Content -Path ".vscode\extensions.json" -Encoding UTF8
    Write-Host "Created: .vscode\extensions.json"
}
else {
    Write-Host "Exists:  .vscode\extensions.json"
}

# ----------------------------------------------------------------------
# 7. Initialize Git repository if needed
# ----------------------------------------------------------------------
if (Get-Command git -ErrorAction SilentlyContinue) {
    if (-not (Test-Path ".git")) {
        git init | Out-Null
        Write-Host "Initialized Git repository." -ForegroundColor Green
    }
    else {
        Write-Host "Git repository already exists."
    }
}
else {
    Write-Host "git was not found in PATH. Skipping git init." -ForegroundColor Yellow
}

# ----------------------------------------------------------------------
# 8. Create uv virtual environment and lock dependencies
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Creating uv environment and resolving dependencies..." -ForegroundColor Cyan
uv sync

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Select the .venv interpreter in VS Code."
Write-Host "  2. Add datasets to data/."
Write-Host "  3. Add future standalone figure files to chapters/chapter_XX_*."
Write-Host ""
