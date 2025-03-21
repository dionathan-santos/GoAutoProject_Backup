# Version Control Guide for GoAuto Project

This guide explains how to properly use Git and DVC (Data Version Control) in this project.

## Overview

In this project, we use:
- **Git** for tracking code, configuration files, and documentation
- **DVC** for tracking data files and ML models

This separation ensures that:
1. Large data files don't bloat the Git repository
2. Data and models are versioned alongside code
3. Reproducibility is maintained across the project

## Setup

1. Install DVC if you haven't already:
   ```bash
   pip install dvc
   ```

2. Clone the repository and pull the data:
   ```bash
   git clone <repository-url>
   cd GoAuto Project
   dvc pull  # This will download the data files tracked by DVC
   ```

## Daily Workflow

### When working with code (Python files, configs, etc.)

Use standard Git commands:
```bash
git add <files>
git commit -m "Your message"
git push
```

### When working with data or models

1. After making changes to data or generating new models:
   ```bash
   # For data changes
   dvc add data/
   
   # For model changes
   dvc add models/
   ```

2. Commit the changes to Git (this commits the .dvc files, not the actual data):
   ```bash
   git add data.dvc models.dvc
   git commit -m "Update data and models"
   ```

3. Push both Git and DVC changes:
   ```bash
   git push
   dvc push
   ```

### Getting the latest changes

1. Pull code changes:
   ```bash
   git pull
   ```

2. Pull data changes:
   ```bash
   dvc pull
   ```

## Important Rules

1. **Never** add large data files directly to Git
2. **Always** use DVC for data and model files
3. **Always** commit .dvc files to Git after running `dvc add`
4. **Remember** to run both `git push` and `dvc push` when sharing your changes

## What's Being Tracked?

### Git Tracks:
- Python code (.py files)
- Configuration files (.yaml, .json)
- Documentation (.md files)
- DVC files (.dvc)
- Small, text-based files

### DVC Tracks:
- Data files (.csv, etc.)
- Model files (.pkl, .h5, etc.)
- Any large binary files

## Troubleshooting

### Missing data files?
```bash
dvc pull
```

### Changes not showing up after pull?
```bash
dvc checkout
```

### Want to switch to a specific version?
```bash
git checkout <commit-or-branch>
dvc checkout
```

## Need Help?

If you encounter any issues with version control, please contact the project maintainer.