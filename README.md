# rag-demo


# FastAPI RAG Demo

A demo of a Retrieval-Augmented Generation (RAG) application using FastAPI, OpenAI, and Qdrant. This project allows you to store documents in a vector database, retrieve information, and ask questions based on stored data.

---

## Project Structure

.
├── app/
│   ├── routers/            # API route definitions
│   ├── services/           # Business logic and integrations with OpenAI & Qdrant
│   ├── utils/              # Utility functions (e.g., text processing)
│   ├── config/             # Configuration settings, including environment variables
│   └── main.py             # Entry point for FastAPI and app setup
├── .env.local              # Environment variables (OpenAI API key, Qdrant DB info)
└── README.md               # Project documentation

---

## Getting Started

### Prerequisites
- **Python** 3.8+
- **FastAPI**
- **Docker** (for running Qdrant DB)
- **OpenAI API Key**

### Running the Project

1. **Clone the repository:**
   git clone <repository-url>
   cd <repository-directory>

2. **Configure environment variables:**
   - Add your OpenAI API key and Qdrant DB information to the `.env.local` file.

3. **Start the FastAPI app:**
   uvicorn app.main:app --reload

---

## Indexing Documents in Qdrant DB

To use Qdrant for document storage and retrieval, follow these steps:

1. **Create a collection:**
    `docs` is already created. set the size to `1536` matching embedding vector size. 
    curl -X POST "http://localhost:9000/api/qdrant/collections/create_collection" -H  "Content-Type: application/json" --data-raw '{"name": "docs", "size": 1536, "distance": "Cosine"}'


2. **Add documents to the collection:**
   - Ensure your document is valid JSON and its content are plain text. Use [JSONLint](https://jsonlint.com/) to validate.
   curl -X 'POST' 'http://localhost:9000/api/index/add_doc' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
        "doc": "your long document text here...",    
        "collection_name": "docs"
    }'

3. **Ask a question based on your documents:**
   - This will query the stored documents and use OpenAI's API to generate an answer.
   
   curl -X POST "http://localhost:8000/ask" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d "{\"question\":\"What is the capital of France?\"}"

---

## API Endpoints

   - Accepts a JSON payload with a question and returns an answer based on stored documents.

   curl -X POST "http://localhost:9000/api/prompt" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"prompt\": \"tell me about company and its mission\", \"collection_name\": \"docs\"}"


---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.

---

Happy querying!

