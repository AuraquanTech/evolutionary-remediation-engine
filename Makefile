# Development workflow

.PHONY: install test lint fmt clean demo

install:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests/ -v --cov=. --cov-report=html

lint:
	flake8 research/ engine/ tests/
	mypy research/ engine/ --ignore-missing-imports

fmt:
	black research/ engine/ tests/
	isort research/ engine/ tests/

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	rm -rf data/*.jsonl data/*.json

research:
	@echo "Running research pipeline..."
	@echo "1. Collecting PRs from GitHub..."
	python -m research.collectors.github_collector
	@echo "2. Extracting patterns..."
	python -m research.extractors.pattern_extractor
	@echo "3. Scoring patterns..."
	python -m research.scoring.confidence_scorer
	@echo "Done! Templates ready."

demo:
	@echo "=== Evolutionary Remediation Engine Demo ==="
	@echo ""
	@echo "1. Loading collected PRs..."
	python -c "import json; prs = [json.loads(l) for l in open('data/raw_prs.jsonl')]; print(f'   Loaded {len(prs)} PRs')"
	@echo ""
	@echo "2. Displaying extracted patterns..."
	python -c "import json; patterns = json.load(open('data/extracted_patterns.json')); print(f'   Found {len(patterns)} patterns'); [print(f'   - {p[\"evidence\"][\"occurrence_count\"]} occurrences') for p in patterns[:5]]"
	@echo ""
	@echo "3. Showing confidence scores..."
	python -c "import json; scored = json.load(open('data/scored_patterns.json')); [print(f'   {p[\"evidence\"][\"occurrence_count\"]} PRs: {p[\"confidence_scores\"][\"overall_confidence\"]:.2f} confidence') for p in scored[:5]]"

help:
	@echo "Available targets:"
	@echo "  make install   - Setup virtual environment"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Lint code"
	@echo "  make fmt       - Format code"
	@echo "  make research  - Run full research pipeline"
	@echo "  make demo      - Show demo output"
	@echo "  make clean     - Clean build artifacts"
