#!/usr/bin/env python3
"""Validate template YAML files."""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class TemplateValidator:
    """Validate YAML templates against schema."""
    
    REQUIRED_FIELDS = ['id', 'name', 'confidence', 'languages']
    OPTIONAL_FIELDS = ['risk_tier', 'evidence', 'pattern', 'pr_template']
    
    @staticmethod
    def validate(template_file: str) -> Tuple[bool, List[str]]:
        """Validate template file."""
        errors = []
        
        try:
            with open(template_file, 'r') as f:
                template = yaml.safe_load(f)
        except Exception as e:
            return False, [f"Failed to load YAML: {e}"]
        
        # Check required fields
        for field in TemplateValidator.REQUIRED_FIELDS:
            if field not in template:
                errors.append(f"Missing required field: {field}")
        
        # Validate confidence
        if 'confidence' in template:
            conf = template['confidence']
            if not isinstance(conf, (int, float)) or not (0 <= conf <= 1):
                errors.append(f"Invalid confidence: {conf} (must be 0-1)")
        
        # Validate languages
        if 'languages' in template:
            if not isinstance(template['languages'], list):
                errors.append("languages must be a list")
        
        return len(errors) == 0, errors
