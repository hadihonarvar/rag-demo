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
    log.info(f">>>>>Getting embedding for {text}")
    res = openai.embeddings.create(model="text-embedding-ada-002", input=[text])
    log.info(f">>>>>Response: {res}")
    return res
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    log.ingo(f">>>>>Response: {response}") 
    return response
    return response['data'][0]['embedding']

# async def get_embedding_tmp(text: str) -> List[float]:
    # model_name = "huggingface/llama-3b"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModel.from_pretrained(model_name)
    
    
    # inputs = tokenizer(text, return_tensors="pt")
    # outputs = model(**inputs)
    # return outputs.last_hidden_state.mean(dim=1).detach().numpy().tolist()

    # text_chunk = "sample product info"
    
    # return get_embedding(text_chunk)

async def get_openAI_image_description():
    response = openai.completions.create(
        model="text-davinci-003",
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "what is in the image?"},
                    {
                        "type": "image",
                        "url": "https://images.unsplash.com/photo-1551316679-9c6ae9dec224"
                    }
                ]
            },
        ],
        max_token=300
    )

    return response.choices[0]

