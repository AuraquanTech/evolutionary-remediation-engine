# Contributing Guide

## Creating New Templates

### 1. Identify a Pattern

Find a recurring fix in 100+ open-source PRs:

```bash
# Search GitHub
https://github.com/search?q=is:pr+is:merged+label:security
```

### 2. Create Template

```bash
cp templates/TEMPLATE.yaml templates/CUSTOM_001.yaml
```

Edit with pattern details:

```yaml
id: CUSTOM_001
name: "Your pattern name"
confidence: 0.85  # Based on research
languages: [javascript]

evidence:
  occurrence_count: 234  # How many PRs
  repo_count: 47         # How many repos
  median_merge_hours: 1.2
```

### 3. Validate

```bash
python -m engine.validators.template_validator templates/CUSTOM_001.yaml
```

### 4. Test

```bash
python -m engine.test_templates --template CUSTOM_001.yaml
```

### 5. Submit PR

```bash
git checkout -b feat/template-custom-001
git add templates/CUSTOM_001.yaml
git commit -m "feat: Add template CUSTOM_001"
git push
```

## Improving Pattern Extraction

The research pipeline can be improved:

- Better diff fingerprinting
- Improved semantic clustering
- More sophisticated confidence scoring

All improvements are welcome!

## Bug Reports

Report issues on GitHub:

https://github.com/AuraquanTech/evolutionary-remediation-engine/issues

## Benchmarking

Run benchmarks to measure performance:

```bash
python -m engine.benchmarks.run_benchmarks
```
