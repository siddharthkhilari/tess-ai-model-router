"""
Base abstract interface for AI model providers (need.md Section 8).
"""

from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, model_id: str) -> str:
        """Generates text response for a given prompt and target model tier."""
        pass
