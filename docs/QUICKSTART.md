# Quick Start Guide

## Installation

### Option 1: Local

```bash
# Clone
git clone https://github.com/AuraquanTech/evolutionary-remediation-engine
cd evolutionary-remediation-engine

# Setup
make install

# Configure
cp .env.example .env
export GITHUB_TOKEN="ghp_your_token_here"
```

### Option 2: Docker

```bash
docker pull auraquantech/evolutionary-remediation:latest

docker run \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  -v /path/to/repo:/repo \
  auraquantech/evolutionary-remediation
```

### Option 3: GitHub Action

```yaml
- uses: AuraquanTech/evolutionary-remediation@v0.1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    confidence: 0.85
```

## Basic Usage

### 1. Scan Repository

```bash
remedy scan --repo /path/to/repo
```

**Output:**
```
Found 42 potential fixes
✓ SECRETS_001: 3 occurrences
✓ DEPS_001: 8 occurrences
✓ UNUSED_001: 15 occurrences
...
```

### 2. Generate Fixes

```bash
remedy fix --repo /path/to/repo --confidence 0.85
```

**Output:**
```
Generated 26 fixes (>0.85 confidence)
✓ tests/test_auth.js: Remove hardcoded secret
✓ package.json: Update lodash 4.17.15 -> 4.17.21
✓ src/index.js: Remove unused import
...
```

### 3. Create PRs (Dry Run)

```bash
remedy pr --repo /path/to/repo --dry-run
```

**Output:**
```
Prepared 26 PRs (dry-run mode)
✓ Branch: fix/secrets-001-auth✓  Title: Security: Remove hardcoded secret
✓ Branch: fix/deps-001-lodash    Title: Security: Update lodash to 4.17.21
✓ Branch: fix/unused-001-utils   Title: Cleanup: Remove unused imports
...
```

### 4. Create Real PRs

```bash
remedy pr --repo /path/to/repo
```

## Configuration

### Via Environment

```bash
export GITHUB_TOKEN="ghp_..."
export CONFIDENCE_THRESHOLD="0.85"
export AUTO_MERGE="false"
export DRY_RUN="true"
```

### Via .env File

```bash
GITHUB_TOKEN=ghp_...
CONFIDENCE_THRESHOLD=0.85
AUTO_MERGE=false
LOG_LEVEL=INFO
LOG_FILE=logs/remediation.log
```

## Templates

### List Templates

```bash
remedy list-templates
```

### Show Template Details

```bash
remedy template-info SECRETS_001
```

**Output:**
```
Template: Remove Hardcoded Secret
Confidence: 0.97 (ULTRA_SAFE)

Evidence:
  Occurrences: 234
  Repositories: 47
  Median merge time: 1.2 hours
  Revert rate: 0%

Example:
  Before: const API_KEY = "abc123";
  After:  const API_KEY = process.env.API_KEY;
```

### Create Custom Template

```bash
cp templates/TEMPLATE.yaml templates/custom.yaml
vim templates/custom.yaml
remedy validate-template templates/custom.yaml
```

## Examples

### Scan and Generate Report

```bash
remedy scan --repo . --report report.json
```

### Fix Only Security Issues

```bash
remedy fix --repo . --tag security --confidence 0.90
```

### Create PRs with Custom Title

```bash
remedy pr --repo . --title-prefix "[bot]"
```

## Troubleshooting

### Rate Limit Error

```
Error: GitHub API rate limited
Solution: Wait 1 hour or increase token scope
```

### No Patterns Matched

```
Error: 0 patterns applicable
Solution: Lower confidence threshold or check file language
```

### PR Creation Failed

```
Error: 422 Validation Failed
Solution: Ensure branch names are valid, no duplicate PRs
```

## Next Steps

1. Read full documentation: [docs/](docs/)
2. Explore templates: [templates/](templates/)
3. Contribute patterns: [CONTRIBUTING.md](CONTRIBUTING.md)
4. Join community: [GitHub Discussions](https://github.com/AuraquanTech/evolutionary-remediation-engine/discussions)
