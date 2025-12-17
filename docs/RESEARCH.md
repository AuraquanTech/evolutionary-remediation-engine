# Research Methodology

## Philosophy

**We don't analyze snapshots. We analyze deltas.**

Traditional SAST tools study "good code" and derive rules.  
We study **how code becomes good** and replicate those transitions.

## The Core Hypothesis

**High-velocity, low-friction changes reveal universal patterns.**

When:
- A fix merges in <2 hours
- With zero discussion
- Never gets reverted
- Appears across 50+ repos

**→ That pattern is universally trusted.**

## Research Pipeline

### Phase 1: Repository Selection

**Criteria (all must pass):**

```python
REQUIREMENTS = {
    "stars": 5000,           # Real adoption
    "contributors": 100,      # Diverse review culture
    "age_years": 2,           # Stable patterns
    "merged_prs": 1000,       # Rich history
    "ci_enabled": True,       # Quality bar
    "tests_present": True,    # Validation
}
```

**Target Categories:**

1. **Meta-tools** (10 repos)
   - ESLint, Prettier, TypeScript-ESLint
   - *Why:* They fix code professionally

2. **Security libraries** (15 repos)
   - jsonwebtoken, helmet, bcrypt, node-forge
   - *Why:* Security-conscious reviews

3. **Frameworks** (25 repos)
   - Next.js, Express, Fastify, Nest
   - *Why:* High scrutiny, production-grade

4. **Build tools** (10 repos)
   - Vite, Webpack, esbuild
   - *Why:* Performance-focused

**Total:** 100 repos, 20K PRs

### Phase 2: PR Evolution Analysis

**For each PR, extract:**

#### 1. Identity
- Repository
- PR number
- Title & description
- Author
- Timestamps (created, merged)

#### 2. Diff Metrics
- Files changed
- Lines added/deleted
- Change scope (single-file, module, cross-module)

#### 3. Friction Metrics
- Time to merge (hours)
- Comment count
- Review count
- Discussion density (comments/line)

#### 4. Stability
- Was reverted? (detect via timeline)
- Revert time (if applicable)
- Caused follow-up fix?

#### 5. Language Patterns
- Title structure
- Explanation style
- Maintainer response sentiment

**Filter criteria:**

```python
HIGH_SIGNAL_PR = (
    merge_time_hours < 24 and
    files_changed < 10 and
    not was_reverted and
    "security" in (title + body).lower()
)
```

**Result:** ~5K high-signal PRs from 20K collected

### Phase 3: Pattern Clustering

**Step 1: Diff Fingerprinting**

```python
# Abstraction levels
LITERAL    = 'const API_KEY = "abc123";'
STRUCTURAL = 'const <VAR> = "<STRING>";'
SEMANTIC   = '<DECLARATION> <VAR> <ASSIGN> <STRING>'
```

We use **structural** abstraction for matching.

**Step 2: Semantic Embeddings**

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(pr_descriptions)
```

**Step 3: DBSCAN Clustering**

```python
from sklearn.cluster import DBSCAN

clustering = DBSCAN(
    eps=0.3,           # Tighter clusters
    min_samples=5,     # Minimum evidence
    metric='cosine'
)
```

**Output:** 50-100 pattern clusters

### Phase 4: Confidence Scoring

**Formula (non-AI, purely statistical):**

```python
def calculate_confidence(pattern):
    # Merge velocity (40% weight)
    # Faster = more trust
    merge_velocity_score = 1.0 - min(pattern.median_merge_hours / 24.0, 1.0)
    
    # Stability (30% weight)
    # No reverts = perfect score
    stability_score = 1.0 - (pattern.revert_rate * 10.0)
    
    # Discussion (15% weight)
    # Low discussion = obvious fix
    discussion_score = 1.0 - min(pattern.discussion_density / 0.5, 1.0)
    
    # Frequency (10% weight)
    # Common = more evidence
    frequency_score = min(log10(pattern.occurrence_count + 1) / 3.0, 1.0)
    
    # Diversity (5% weight)
    # Cross-repo = universal
    diversity_score = min(pattern.repo_count / 20.0, 1.0)
    
    # Weighted sum
    confidence = (
        0.40 * merge_velocity_score +
        0.30 * stability_score +
        0.15 * discussion_score +
        0.10 * frequency_score +
        0.05 * diversity_score
    )
    
    return max(0.0, min(1.0, confidence))
```

**Risk Tiers:**

| Tier | Confidence | Auto-PR | Examples |
|------|------------|---------|----------|
| Ultra-safe | ≥0.95 | ✅ Yes | Remove unused import, bump patch |
| Safe | ≥0.85 | ✅ Yes | Add null check, replace deprecated API |
| Moderate | ≥0.70 | ❌ No | Add validation, refactor error handling |
| Risky | <0.70 | ❌ No | Complex logic, architectural changes |

### Phase 5: Template Generation

**Format:**

```yaml
id: SECRETS_001
name: "Remove Hardcoded Secret"
confidence: 0.97

evidence:
  occurrence_count: 234
  repo_count: 47
  median_merge_hours: 1.2
  median_discussion_density: 0.02
  revert_rate: 0.0
  
pattern:
  before: |
    const {{var_name}} = "{{secret_value}}";
  after: |
    const {{var_name}} = process.env.{{env_var}};
    
companion_changes:
  - add_to_gitignore: [".env"]
  - create_env_example: true
  
pr_template:
  title: "Remove hardcoded secret in {{file}}"
  body: |
    Removes hardcoded credential and loads from environment.
    
    **Security impact:** Prevents credential exposure in version control.
    
    **Evidence:** 234 similar fixes across 47 repos, 0% revert rate.
```

## Validation

### Held-Out Testing

**Method:**
- Hold out 20% of repos
- Train on 80%
- Test patterns on held-out repos
- Measure precision/recall

**Metrics:**

```python
PRECISION = true_matches / (true_matches + false_matches)
RECALL = true_matches / total_applicable_cases
F1 = 2 * (precision * recall) / (precision + recall)
```

**Target:** F1 > 0.90

### Manual Review

Top 10 patterns reviewed by:
- Senior engineers
- Security researchers
- Open-source maintainers

**Approval threshold:** 100% consensus

## Continuous Improvement

**Learning loop:**

1. Deploy patterns to production
2. Track customer PR outcomes
   - Merge rate
   - Revert rate
   - Time to merge
3. Update confidence scores monthly
4. Retire patterns with <80% merge rate
5. Discover new patterns from customer data (with consent)

**Bayesian update:**

```python
# Initial: Use research priors
initial_confidence = research_prior

# After 100 customer PRs:
updated_confidence = (
    0.7 * research_prior +
    0.3 * customer_actual
)

# After 1000 customer PRs:
final_confidence = (
    0.3 * research_prior +
    0.7 * customer_actual
)
```

## Legal Compliance

### What We Analyze

✅ **Public repositories** (GitHub ToS permits)  
✅ **Metadata** (merge times, discussion density)  
✅ **Structural patterns** (not code copying)  
✅ **Cited sources** (link to original PRs)  

### What We Don't Use

❌ **Private repositories**  
❌ **Customer code** (without explicit consent)  
❌ **Proprietary logic**  
❌ **Personal data** (GDPR compliant)  

## Research Output

**Deliverables:**

1. **Template Library** (50+ patterns)
   - YAML format
   - Confidence scores
   - Evidence citations

2. **Research Paper** (peer-reviewed)
   - Methodology
   - Results
   - Reproducibility

3. **Open Dataset** (anonymized)
   - PR metadata
   - Pattern clusters
   - Evaluation metrics

[Next: Template Format →](TEMPLATES.md)