"""
JSON Schemas for validating LLM output before it reaches a client.

The model is asked for JSON, but a model can always return prose, truncated
JSON, or valid JSON with the wrong shape. Every AI response in this service is
checked against one of these schemas and rejected if it does not conform, so a
malformed generation becomes a retry rather than a broken API response.
"""

# Reasoning: a short personalised explanation of why a career fits a profile.
REASONING_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "CareerReasoning",
    "type": "object",
    "properties": {
        "reasoning": {"type": "string", "minLength": 20, "maxLength": 1200},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "key_factors": {
            "type": "array",
            "items": {"type": "string", "minLength": 1, "maxLength": 120},
            "minItems": 1,
            "maxItems": 5,
        },
    },
    "required": ["reasoning"],
    "additionalProperties": False,
}

# Roadmap: an ordered learning path, each step with an effort estimate.
ROADMAP_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LearningRoadmap",
    "type": "object",
    "properties": {
        "steps": {
            "type": "array",
            "minItems": 1,
            "maxItems": 12,
            "items": {
                "type": "object",
                "properties": {
                    "step": {"type": "integer", "minimum": 1},
                    "title": {"type": "string", "minLength": 3, "maxLength": 200},
                    "description": {"type": "string", "maxLength": 1000},
                    "duration": {"type": "string", "maxLength": 60},
                    "resources": {
                        "type": "array",
                        "items": {"type": "string", "maxLength": 200},
                        "maxItems": 6,
                    },
                },
                "required": ["step", "title"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["steps"],
    "additionalProperties": False,
}

# Skill gap: what the user already has, what is missing, and what to do next.
SKILL_GAP_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "SkillGapAnalysis",
    "type": "object",
    "properties": {
        "summary": {"type": "string", "minLength": 10, "maxLength": 1200},
        "priority_order": {
            "type": "array",
            "items": {"type": "string", "maxLength": 120},
            "maxItems": 15,
        },
        "estimated_months": {"type": "number", "minimum": 0, "maximum": 120},
    },
    "required": ["summary"],
    "additionalProperties": False,
}
