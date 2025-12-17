# Deployment Guide

## Development Setup

```bash
# Clone
git clone https://github.com/AuraquanTech/evolutionary-remediation-engine
cd evolutionary-remediation-engine

# Setup environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup configuration
cp .env.example .env
export GITHUB_TOKEN="ghp_your_token_here"
```

## Running the Research Pipeline

### Step 1: Collect PRs

```bash
python -m research.collectors.github_collector
```

**Output:** `data/raw_prs.jsonl`

### Step 2: Extract Patterns

```bash
python -m research.extractors.pattern_extractor
```

**Output:** `data/extracted_patterns.json`

### Step 3: Score Patterns

```bash
python -m research.scoring.confidence_scorer
```

**Output:** `data/scored_patterns.json`

### Step 4: Generate Templates

Templates are created manually from top patterns:

```bash
# Edit template
vim templates/custom_001.yaml

# Validate
python -m engine.validators.template_validator templates/custom_001.yaml
```

## Running the Engine

### Scan Repository

```bash
python -m engine.cli scan --repo /path/to/repo
```

### Generate Fixes

```bash
python -m engine.cli fix --repo /path/to/repo --confidence 0.85
```

### Create PRs

```bash
# Dry run first
python -m engine.cli pr --repo /path/to/repo --dry-run

# Create actual PRs
python -m engine.cli pr --repo /path/to/repo
```

## Production Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "engine.cli"]
```

```bash
docker build -t evolutionary-remediation-engine .
docker run -e GITHUB_TOKEN=$GITHUB_TOKEN -v /repos:/repos evolutionary-remediation-engine
```

### GitHub Actions

```yaml
name: Evolutionary Remediation

on: [push]

jobs:
  remediate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: AuraquanTech/evolutionary-remediation@v0.1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          confidence: 0.85
```

## Monitoring

### Metrics to Track

```
- PRs created per week
- Merge rate (%)
- Revert rate (%)
- Average merge time (hours)
- Most common patterns
- False positive rate
```

### Logging

```bash
export LOG_LEVEL=DEBUG
export LOG_FILE=logs/remediation.log
```

## Troubleshooting

### Rate Limit Errors

```
403 API Rate Limited
Solution: Increase GITHUB_TOKEN scope or wait for reset
```

### Pattern Matching Failures

```
No patterns matched
Solution: Check pattern compatibility with file language
```

### PR Creation Failures

```
422 Validation Failed
Solution: Ensure branch name is valid, no duplicate PRs
```
