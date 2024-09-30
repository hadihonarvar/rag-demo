# openai_service.py
import openai
from typing import List
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

async def get_embedding(text: str) -> List[float]:
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response
    return response['data'][0]['embedding']
