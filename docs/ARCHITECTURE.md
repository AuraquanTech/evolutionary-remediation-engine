# Architecture Overview

## System Design

Evolutionary Remediation Engine consists of two major subsystems:

### 1. Research Pipeline (Offline)

**Purpose:** Extract high-confidence remediation patterns from historical PR data

**Components:**

```
┌─────────────────────────────────────────────────────┐
│  GitHub API Collector                                │
│  ─────────────────────                                │
│  • Rate-limited PR collection                        │
│  • Metadata extraction (merge time, discussion)      │
│  • Revert detection                                  │
│  • Output: raw_prs.jsonl                             │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  Pattern Extractor                                   │
│  ─────────────────                                    │
│  • Diff fingerprinting (AST-based)                   │
│  • Semantic clustering (DBSCAN)                      │
│  • Cross-repo validation                             │
│  • Output: extracted_patterns.json                   │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  Confidence Scorer                                   │
│  ──────────────────                                  │
│  • Evidence-based scoring (non-AI)                   │
│  • Risk tier assignment                              │
│  • Template generation                               │
│  • Output: templates/*.yaml                          │
└─────────────────────────────────────────────────────┘
```

**Timeline:** Run once per month (continuous improvement)

### 2. Remediation Engine (Online)

**Purpose:** Apply patterns to customer code and generate PRs

**Components:**

```
┌─────────────────────────────────────────────────────┐
│  Scanner Integration                                 │
│  ───────────────────                                 │
│  • SARIF parser (universal)                          │
│  • Semgrep, Snyk, GitHub, Checkmarx support         │
│  • Finding normalization                             │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  Template Matcher                                    │
│  ───────────────                                     │
│  • AST-based pattern matching                        │
│  • Confidence thresholding                           │
│  • Context extraction                                │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  Fix Generator                                       │
│  ──────────────                                      │
│  • Template instantiation                            │
│  • Syntax validation                                 │
│  • Test execution (optional)                         │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  PR Creator                                          │
│  ──────────                                          │
│  • GitHub API integration                            │
│  • Evidence-based PR text                            │
│  • Audit trail logging                               │
└─────────────────────────────────────────────────────┘
```

## Data Flow

### Research Phase

1. **Input:** Curated list of 100 high-quality repos
2. **Collection:** 20K PRs (security-focused)
3. **Filtering:** High-signal PRs only (<24h merge, not reverted)
4. **Clustering:** Group similar changes
5. **Scoring:** Calculate confidence scores
6. **Output:** 50+ production-ready templates

### Remediation Phase

1. **Input:** Customer repository
2. **Scan:** Run SAST tool (Semgrep, Snyk, etc.)
3. **Match:** Find applicable templates
4. **Generate:** Create fixes
5. **Validate:** Syntax + tests
6. **PR:** Create pull request
7. **Learn:** Track merge/revert for continuous improvement

## Technology Stack

- **Language:** Python 3.9+
- **ML:** sentence-transformers (embeddings)
- **Clustering:** scikit-learn (DBSCAN)
- **AST:** tree-sitter (multi-language)
- **API:** PyGithub
- **Storage:** JSONL (simple), PostgreSQL (optional)

## Scalability

### Research Pipeline

- **Collection:** 500 PRs/hour (GitHub rate limit)
- **Processing:** 10K PRs in ~2 hours (CPU-bound)
- **Storage:** ~100MB per 10K PRs

### Remediation Engine

- **Matching:** O(n*m) where n=findings, m=templates
- **Optimization:** Template indexing by vulnerability type
- **Throughput:** 1000+ findings/minute

## Security

- **No customer code training:** Privacy by design
- **Public data only:** Research uses open-source repos
- **Audit logs:** Immutable record of all PRs
- **Human-in-the-loop:** Never auto-merge

[Next: Research Methodology →](RESEARCH.md)