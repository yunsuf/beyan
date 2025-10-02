from __future__ import annotations
from typing import Any, Dict, Optional

from .registry import ModelRegistry
from .policy import RoutingPolicy


class SmartRouter:
    """
    Simple rule-based Smart Router for Phase 1.
    - Selects a model using RoutingPolicy rules + ModelRegistry candidates
    - No LLM coordinator in this phase (can be added later)
    """

    def __init__(self, registry: ModelRegistry, policy: RoutingPolicy):
        self.registry = registry
        self.policy = policy

    def select(self, task: str, features: Dict[str, Any]) -> Dict[str, Any]:
        required_caps = features.get("required_capabilities", [])
        candidates = self.registry.candidates(required_caps)
        match = self.policy.match(task, features, candidates)
        if match and match.get("choice"):
            key = match["choice"]
            m = self.registry.get_model(key) or {}
            return {
                "portfolio_key": key,
                "provider": m.get("provider"),
                "model_name": m.get("name"),
                "rule": match.get("rule"),
                "reason": match.get("reason"),
            }
        # fallback
        m = self.registry.get_default_model() or {}
        # NOTE: registry.get_default_model returns {"name": <remote_model>} so we need key
        # We can't recover portfolio key here easily; mark as default
        return {
            "portfolio_key": "<default>",
            "provider": m.get("provider"),
            "model_name": m.get("name"),
            "rule": "default",
            "reason": "no rule matched",
        }
