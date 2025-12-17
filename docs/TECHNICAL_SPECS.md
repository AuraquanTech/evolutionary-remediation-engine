# Technical Specifications

## Architecture

### System Components

1. **GitHub PR Collector**
   - Rate-limited API calls (60 req/hour)
   - Pagination support (100+ repos, 10K+ PRs)
   - Security metadata extraction
   - Error recovery + retry logic

2. **Pattern Extractor**
   - Diff fingerprinting (3-level abstraction)
   - Semantic embeddings (sentence-transformers)
   - DBSCAN clustering (eps=0.5, min_samples=5)
   - Cross-repo validation

3. **Confidence Scorer**
   - Non-AI statistical model
   - 5-component weighted formula
   - Risk tier assignment
   - Auditable scoring

4. **Template Engine**
   - YAML-based template system
   - AST-based pattern matching
   - Variable substitution
   - Syntax validation

5. **PR Generator**
   - GitHub API integration
   - Human-in-the-loop approval
   - Audit trail logging
   - Revert detection

## Performance Specifications

### Research Pipeline
- Collection: 500 PRs/hour (GitHub rate limited)
- Analysis: 10K PRs in ~2 hours (CPU-bound)
- Storage: ~100MB per 10K PRs
- Update frequency: Monthly

### Remediation Engine
- Template matching: O(n*m) where n=findings, m=templates
- Throughput: 1000+ findings/minute
- PR creation: <5 seconds per PR
- End-to-end: <2 minutes for typical repo

## Data Models

### PR Metadata
```python
@dataclass
class PRMetadata:
    repo: str
    owner: str
    pr_number: int
    merge_time_hours: float
    is_security_related: bool
    has_revert: bool
    revert_time_hours: Optional[float]
```

### Pattern
```python
@dataclass
class FixTemplate:
    id: str
    name: str
    confidence: float
    evidence: PatternEvidence
    before: str
    after: str
    language: str
```

## Confidence Formula

```
confidence = 
  0.40 * merge_velocity_score +
  0.30 * stability_score +
  0.15 * discussion_score +
  0.10 * frequency_score +
  0.05 * diversity_score
```

Where:
- `merge_velocity_score` = 1 - (hours / 24)
- `stability_score` = 1 - (revert_rate * 10)
- `discussion_score` = 1 - (density * 2)
- `frequency_score` = log10(count) / 3
- `diversity_score` = repos / count * 0.5

## API Endpoints (Future)

### Public API

```
GET  /api/templates              # List templates
GET  /api/templates/:id          # Get template
POST /api/scan                   # Scan repo
POST /api/fix                    # Generate fixes
POST /api/pr                     # Create PRs
```

## Security

- No storage of customer code
- Read-only GitHub API access
- Audit logs of all PRs
- Optional self-hosted deployment
- SOC 2 compliance (roadmap)

## Scalability

### Horizontal
- Stateless design (easy scaling)
- Load balance across servers
- Queue-based PR processing

### Vertical
- Multi-threaded pattern matching
- Batch processing for templates
- Cached embeddings

## Testing

- Unit tests: >80% coverage
- Integration tests: Full pipeline
- Benchmarks: Performance tracking
- E2E tests: On real repositories
