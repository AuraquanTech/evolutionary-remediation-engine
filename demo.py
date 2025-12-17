#!/usr/bin/env python3
"""
Demo: Complete evolutionary remediation workflow.
"""

import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show_demo():
    """Show complete demo workflow."""
    print("\n" + "="*60)
    print("EVOLUTIONARY REMEDIATION ENGINE - DEMO")
    print("="*60)
    
    # 1. Load data
    print("\n[PHASE 1] Data Collection")
    print("-" * 40)
    
    data_dir = Path("data")
    if (data_dir / "raw_prs.jsonl").exists():
        with open(data_dir / "raw_prs.jsonl") as f:
            prs = [json.loads(line) for line in f if line.strip()]
        print(f"✓ Loaded {len(prs)} PRs from GitHub")
        print(f"  - Security-related: {sum(1 for p in prs if p['is_security_related'])}")
        print(f"  - Average merge time: {sum(p['merge_time_hours'] for p in prs)/len(prs):.1f}h")
    
    # 2. Show patterns
    print("\n[PHASE 2] Pattern Extraction")
    print("-" * 40)
    
    if (data_dir / "extracted_patterns.json").exists():
        with open(data_dir / "extracted_patterns.json") as f:
            patterns = json.load(f)
        print(f"✓ Extracted {len(patterns)} patterns")
        for i, p in enumerate(patterns[:3], 1):
            print(f"\n  Pattern {i}:")
            print(f"    - Size: {p['size']} PRs")
            print(f"    - Repos: {p['evidence']['repo_count']} different repos")
            print(f"    - Median merge: {p['evidence']['median_merge_hours']:.1f}h")
    
    # 3. Show templates
    print("\n[PHASE 3] Template Library")
    print("-" * 40)
    
    template_dir = Path("templates")
    templates = list(template_dir.glob("*.yaml"))
    print(f"✓ {len(templates)} templates ready")
    for tmpl in templates[:3]:
        print(f"  - {tmpl.stem}")
    
    # 4. Show confidence scores
    print("\n[PHASE 4] Confidence Scoring")
    print("-" * 40)
    print("✓ Non-AI statistical model (fully auditable)")
    print("  - Merge velocity: 40% weight")
    print("  - Stability: 30% weight")
    print("  - Discussion: 15% weight")
    print("  - Frequency: 10% weight")
    print("  - Diversity: 5% weight")
    
    # 5. Show CLI
    print("\n[PHASE 5] Remediation Engine")
    print("-" * 40)
    print("✓ CLI Ready")
    print("  $ remedy scan --repo /path/to/repo")
    print("  $ remedy fix --repo /path/to/repo --confidence 0.85")
    print("  $ remedy pr --repo /path/to/repo --dry-run")
    
    print("\n" + "="*60)
    print("Demo complete! Next steps:")
    print("  1. Run: make research")
    print("  2. Review: data/scored_patterns.json")
    print("  3. Deploy: docker build -t evolutionary-remediation .")
    print("="*60 + "\n")

if __name__ == "__main__":
    show_demo()
