# Advanced RAG System

This project is an advanced Retrieval-Augmented Generation (RAG) system. It combines document retrieval with generative AI to answer questions or provide insights based on your data.

## Features

- Document ingestion and indexing
- REST API for querying and retrieval
- Dockerized deployment
- Sample corpus for testing

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Python 3.8+ (for local development)

### Running with Docker

```sh
docker compose up --build
```

The API will be available at [http://localhost:8000](http://localhost:8000).

### Local Development

1. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```
2. Activate the environment:
    - Windows:
      ```sh
      .venv\Scripts\activate
      ```
    - macOS/Linux:
      ```sh
      source .venv/bin/activate
      ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Run the API (example for FastAPI):
    ```sh
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

## Project Structure

- `app/` - Main application code
- `app/data/` - Sample corpus and data files
- `Dockerfile` - Container build instructions
- `docker-compose.yml` - Multi-container orchestration
- `.env` - Environment variables (not committed)
- `.gitignore` - Files and folders to ignore in git

## License

MIT License

---

**Sorry for the late submissions. Kindly consider the project for evaluation.**

*For questions or contributions, please open an issue or pull request.*