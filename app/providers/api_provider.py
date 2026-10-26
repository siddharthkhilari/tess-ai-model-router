"""
API AI Provider (need.md Section 8, 25).
Optional adapter for external real AI API providers (OpenAI / HuggingFace / compatible endpoints).
"""

import httpx
from app.providers.base import BaseAIProvider
from app.providers.demo_provider import DemoProvider
from app.core.config import AI_API_KEY, AI_PROVIDER

class APIProvider(BaseAIProvider):
    def __init__(self):
        self.fallback = DemoProvider()
        self.api_key = AI_API_KEY
        self.provider = AI_PROVIDER

    def generate(self, prompt: str, model_id: str) -> str:
        if not self.api_key:
            # Fallback to demo mode if no API key is provided
            return self.fallback.generate(prompt, model_id)

        try:
            # Demonstration of OpenAI-compatible chat completion
            # Mapping tier to models
            model_map = {
                "small": "gpt-4o-mini",
                "medium": "gpt-3.5-turbo",
                "large": "gpt-4o"
            }
            target_model = model_map.get(model_id, "gpt-4o-mini")

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": target_model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.3
            }

            with httpx.Client(timeout=15.0) as client:
                res = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"API Error ({res.status_code}): Falling back to demo mode.\n\n" + self.fallback.generate(prompt, model_id)
        except Exception as e:
            return f"Provider exception ({str(e)}). Falling back to demo response.\n\n" + self.fallback.generate(prompt, model_id)
