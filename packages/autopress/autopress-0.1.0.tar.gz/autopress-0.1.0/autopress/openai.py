from openai import OpenAI
import autopress.settings as settings

import logging
logger = logging.getLogger()

try:
    client = OpenAI(api_key=settings.getenv("OPENAI_API_KEY"))
except Exception as e:
    client = None

def generate(docstring: str) -> str:
    """Use this method to generate a docstring from a method signature.

    Args:
        docstring (str): the method signature
    """
    content = f"Docstring:'''{docstring}'''"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": settings.getenv("INSTRUCTIONS")
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-4-0125-preview",
    )
    return chat_completion.choices[0].message.content