from app.llm.client import LLMClient


def test_llm_generation():
    client = LLMClient()

    response = client.generate(
        "Explain what a product comparison system does in one sentence."
    )

    assert response
    assert isinstance(response, str)