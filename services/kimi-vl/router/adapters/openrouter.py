from __future__ import annotations
import base64
from typing import Any, Dict, List, Optional
import httpx


class OpenRouterAdapter:
    """
    Minimal OpenRouter adapter for JSON extraction with vision inputs.
    """

    def __init__(self, api_key: Optional[str], base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.chat_url = f"{self.base_url}/chat/completions"
        timeout = httpx.Timeout(120.0)
        self.client = httpx.AsyncClient(timeout=timeout)

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def extract_json(
        self,
        prompt: str,
        images: List[bytes],
        model_name: str,
        temperature: float = 0.1,
    ) -> Dict[str, Any]:
        if not self.is_configured():
            raise RuntimeError("OpenRouterAdapter is not configured (missing API key)")

        contents: List[Dict[str, Any]] = []
        for img in images:
            b64 = base64.b64encode(img).decode("utf-8")
            contents.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
        contents.append({"type": "text", "text": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": model_name,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": contents}
            ],
        }
        resp = await self.client.post(self.chat_url, headers=headers, json=body)
        resp.raise_for_status()
        response_json = resp.json()
        message_content = response_json["choices"][0]["message"]["content"]
        json_content_str = message_content.strip().lstrip("```json").rstrip("```")
        import json as _json
        return {
            "raw": message_content,
            "extracted_fields": _json.loads(json_content_str),
            "provider": "openrouter",
            "model": model_name,
        }
