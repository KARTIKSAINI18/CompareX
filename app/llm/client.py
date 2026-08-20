from openai import OpenAI

from app.core.config import settings


class LLMClient:
    """Client for communicating with an OpenAI-compatible LLM endpoint."""

    def __init__(self):
        if not settings.llm_base_url:
            raise ValueError("LLM_BASE_URL is not configured.")

        if not settings.llm_model:
            raise ValueError("LLM_MODEL is not configured.")

        self.client = OpenAI(
            api_key=settings.llm_api_key or "ollama",
            base_url=settings.llm_base_url,
        )

        self.model = settings.llm_model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("LLM returned an empty response.")

        return content