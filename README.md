# FastAPI RAG Demo

A demo of a basic Retrieval-Augmented Generation (RAG) application using FastAPI, OpenAI, and Qdrant. This project allows you to store documents in a vector database, retrieve information, and ask questions based on stored data.

---

## Getting Started

### Prerequisites
- **Python** 3.9+
- **FastAPI**
- **Qdrant API key**
- **OpenAI API Key**

### Running the Project

1. **Clone the repository:**

   ```
   git clone git@github.com:hadihonarvar/rag-demo.git
   ```

   ```
   cd rag-demo
   ```

2. **Configure environment variables:**
   - Add your OpenAI API key and Qdrant DB information to the `.env.local` file.
   - For Qdrant, it is already set up a free tier, change it to your own instance if needed.
   - For OpenAI api key, find yours here: [OPEN AI APIKEY](https://platform.openai.com/api-keys)

3. **Start the FastAPI app:**

   ```
   bash ./run.sh
   ```

---

## Indexing Documents in Qdrant DB

To use Qdrant for document storage and retrieval, follow these steps:

1. **Create a collection:**
    `docs` is already created. set the size to `1536` matching embedding vector size. 
    ```
    curl -X POST "http://localhost:9000/api/qdrant/collections/create_collection" -H  "Content-Type: application/json" --data-raw '{"name": "docs", "size": 1536, "distance": "Cosine"}'
    ```
    


2. **Add documents to the collection:**
   - Ensure your document is valid JSON and its content are plain text. Use [JSONLint](https://jsonlint.com/) to validate.
   ```
   curl -X 'POST' 'http://localhost:9000/api/index/add_doc' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
        "doc": "your long document text here...",    
        "collection_name": "docs"
    }'
    ```

3. **Ask a question based on your documents:**
   - This will query the stored documents and use OpenAI's API to generate an answer.
   ```
   curl -X POST "http://localhost:8000/ask" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d "{\"question\":\"What is the capital of France?\"}"
    ```
---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.

---

Happy querying!
