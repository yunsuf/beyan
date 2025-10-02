import os
from typing import Any, Dict, List, Optional
import yaml


class ModelRegistry:
    """Loads and provides access to the model portfolio (config/models.yml)."""

    def __init__(self, portfolio_path: str = "config/models.yml"):
        self.portfolio_path = portfolio_path
        self.providers: Dict[str, Dict[str, Any]] = {}
        self.models: Dict[str, Dict[str, Any]] = {}
        self.defaults: Dict[str, Any] = {}
        self.constraints: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.portfolio_path):
            raise FileNotFoundError(f"Model portfolio not found: {self.portfolio_path}")
        with open(self.portfolio_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        self.providers = data.get("providers", {})
        self.models = data.get("models", {})
        self.defaults = data.get("defaults", {})
        self.constraints = data.get("constraints", {})

    def get_provider(self, name: str) -> Optional[Dict[str, Any]]:
        return self.providers.get(name)

    def get_model(self, name: str) -> Optional[Dict[str, Any]]:
        return self.models.get(name)

    def candidates(self, capabilities: List[str]) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for mname, m in self.models.items():
            caps = set(m.get("capabilities", []))
            if all(c in caps for c in capabilities):
                result.append({"name": mname, **m})
        return result

    def get_default_model(self) -> Optional[Dict[str, Any]]:
        # pick first fallback or any model
        fallbacks = self.defaults.get("fallbacks", [])
        for fb in fallbacks:
            m = self.get_model(fb)
            if m:
                return {"name": fb, **m}
        # otherwise first in models
        for mname, m in self.models.items():
            return {"name": mname, **m}
        return None
