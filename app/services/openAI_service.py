# openai_service.py
import openai
from typing import List
from app.config import settings
from app.utils.logger import log

openai.api_key = settings.OPENAI_API_KEY

# ❯ curl https://api.openai.com/v1/embeddings \           
#   -H "Authorization: Bearer $APIKEY" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "input": "The food was delicious and the waiter...",
#     "model": "text-embedding-ada-002",
#     "encoding_format": "float"
#   }'

async def get_openAI_embedding(text: str):
    log.info(f"Getting embedding for {text}")
    response = openai.embeddings.create(model="text-embedding-ada-002", input=[text]) # embedding size: 1536
    log.info(f"Response: {len(response.data[0].embedding)}") 
    return response.data[0].embedding


async def get_openAI_response(conversation):
    log.info(f"Getting response for conversation: {conversation}")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=100,
        temperature=0.5
    )
    return response

