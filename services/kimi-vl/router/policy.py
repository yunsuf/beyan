from __future__ import annotations
import os
from typing import Any, Dict, List, Optional
import yaml


class RoutingPolicy:
    """Loads config/routing.yml and evaluates simple rule-based routing.

    Rules format (strings with simple operators):
      - "task in [\"header_extraction\", \"line_items\"]"
      - "doc_type == \"invoice\""
      - "page_count <= 3"
      - "budget in [\"low\", \"medium\"]"
    Supports 'all' and 'any' blocks under 'when'.
    """

    def __init__(self, routing_path: str = "config/routing.yml"):
        self.routing_path = routing_path
        self.rules: List[Dict[str, Any]] = []
        self.fallbacks: Dict[str, Any] = {}
        self.retry_policy: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.routing_path):
            raise FileNotFoundError(f"Routing policy not found: {self.routing_path}")
        with open(self.routing_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        self.rules = data.get("rules", [])
        self.fallbacks = data.get("fallbacks", {})
        self.retry_policy = data.get("retry_policy", {"attempts": 1, "backoff_ms": 0})

    def _eval_condition(self, expr: str, ctx: Dict[str, Any]) -> bool:
        expr = str(expr).strip()
        # Supported patterns: key in [..], key == value, key <= value, key >= value, key > value, key < value
        try:
            if " in " in expr:
                left, right = expr.split(" in ", 1)
                left = left.strip()
                right = right.strip()
                # Expect right like ["a","b"] or ['a','b']
                if right.startswith("[") and right.endswith("]"):
                    items_raw = right[1:-1].strip()
                    items = [i.strip().strip("'\"") for i in items_raw.split(",") if i.strip()]
                    return ctx.get(left) in items
                else:
                    return False
            for op in ["<=", ">=", "==", ">", "<"]:
                if op in expr:
                    left, right = expr.split(op, 1)
                    left = left.strip()
                    right = right.strip().strip("'\"")
                    lval = ctx.get(left)
                    # Try numeric compare when possible
                    try:
                        rval_num = float(right)
                        lval_num = float(lval)
                        if op == "<=":
                            return lval_num <= rval_num
                        if op == ">=":
                            return lval_num >= rval_num
                        if op == ">":
                            return lval_num > rval_num
                        if op == "<":
                            return lval_num < rval_num
                    except Exception:
                        # fallback to string compare for == only
                        if op == "==":
                            return str(lval) == str(right)
                        return False
            return False
        except Exception:
            return False

    def _match_when(self, when: Dict[str, Any], ctx: Dict[str, Any]) -> bool:
        if "all" in when:
            return all(self._eval_condition(expr, ctx) for expr in when["all"])
        if "any" in when:
            lst = when["any"]
            return any(self._eval_condition(expr, ctx) for expr in lst)
        return False

    def match(self, task: str, features: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        ctx = {**features, "task": task}
        cand_names = {c["name"] for c in candidates}
        for rule in self.rules:
            when = rule.get("when", {})
            if self._match_when(when, ctx):
                choice = rule.get("choose")
                if choice and choice in cand_names:
                    return {"rule": rule.get("name", "unknown"), "choice": choice, "reason": f"matched:{rule.get('name')}"}
        return None
