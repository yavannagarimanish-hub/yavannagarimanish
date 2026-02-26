# $name

> $headline

$mission

## Focus Areas
$focus_areas

## Current Projects
$current_projects

## Impact
$impact_metrics

## Contact
$contact

## Repository Automation
This README is generated from `profile.json` using `scripts/generate_readme.py`.

### Why this structure?
- Keeps profile data and presentation separate.
- Enables consistent updates and CI validation.
- Reduces manual editing errors.

## Local Development
```bash
python3 scripts/generate_readme.py
```

## Quality Gate
The CI workflow (`.github/workflows/readme-sync.yml`) validates that README output stays in sync with source data.
