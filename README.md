# CompareX

CompareX is an AI-powered product comparison and recommendation assistant.

It allows users to search, compare, and get recommendations for smartphones using product information and relevant product documentation.

The system combines semantic product search, requirement extraction, recommendation, comparison, document retrieval, and Retrieval-Augmented Generation (RAG).

---
<img width="1186" height="680" alt="Screenshot 2026-08-20 141740" src="https://github.com/user-attachments/assets/75f58298-8d3a-4039-b327-eb5669ba3d2e" />

<img width="1012" height="584" alt="Screenshot 2026-08-20 141823" src="https://github.com/user-attachments/assets/1bd49e11-6b5b-458a-b313-09b4204fcea9" />

<img width="1047" height="687" alt="Screenshot 2026-08-20 141905" src="https://github.com/user-attachments/assets/6536190e-6557-4858-b119-9883d974f904" />



## Features

- Natural-language product search
- Product requirement extraction
- Semantic product retrieval
- Smartphone recommendations
- Product comparison
- Query intent planning
- Battery, RAM, storage, price, rating and other specification handling
- Product-document retrieval
- Document-based RAG
- Combined product + document context
- Grounded LLM responses
- FastAPI backend
- Browser-based frontend
- MongoDB Atlas Vector Search
- Sentence Transformer embeddings
- Local Qwen model through Ollama

---

## Architecture

```text
                         User
                           |
                           v
                    CompareX Web UI
                           |
                           v
                       FastAPI
                           |
                           v
                  CompareX Service
                           |
              +------------+------------+
              |                         |
              v                         v
       Query Understanding       Document Retrieval
              |                         |
              v                         v
      Product Retrieval          MongoDB Vector Search
              |                         |
              v                         v
       Product Context          Manual / Document Context
              |                         |
              +------------+------------+
                           |
                           v
                    Combined Context
                           |
                           v
                         Qwen
                           |
                           v
                    Grounded Answer






How It Works
1. User Query

The user asks a natural-language question such as:

Recommend a Samsung phone under 30000 with good camera
2. Requirement Extraction

CompareX extracts useful requirements such as:

category
brand
platform
maximum price
minimum RAM
minimum storage
battery requirements
camera preference
performance preference
3. Query Planning

The system determines the user's intent.

Examples:

Which phone has the largest battery?
        -> FIND_BEST


Compare Samsung and OnePlus phones
        -> COMPARE


Recommend a phone with a good camera
        -> RECOMMEND


Show smartphones with large batteries
        -> SEARCH
4. Product Retrieval

Product embeddings are generated using:

sentence-transformers/all-MiniLM-L6-v2

The embeddings are stored in MongoDB Atlas and searched using MongoDB Vector Search.

5. Product Matching and Ranking

Retrieved products can be filtered and ranked according to requirements such as:

price
RAM
storage
battery
rating
camera
performance
brand
platform
6. Document Retrieval

Product manuals and other product documents are:

PDF
 ↓
Chunks
 ↓
Embeddings
 ↓
MongoDB
 ↓
MongoDB Vector Search

This allows CompareX to retrieve relevant information from product documentation.

7. RAG

The system combines:

Product Context
      +
Document Context
      ↓
Combined Context
      ↓
Qwen
      ↓
Final Answer

The LLM is instructed to use only the supplied context for factual product claims.

Technology Stack
Component	Technology
Language	Python
Backend	FastAPI
Database	MongoDB Atlas
Vector Search	MongoDB Atlas Vector Search
Embeddings	Sentence Transformers
Embedding Model	all-MiniLM-L6-v2
LLM	Qwen through Ollama
RAG	Custom lightweight RAG pipeline
Frontend	HTML, CSS, JavaScript
Validation	Pydantic
Data

The project uses a processed Amazon smartphone dataset containing more than 1,500 usable smartphone products.

Product data includes fields such as:

product ID
name
brand
category
description
specifications
price
rating
review count

Product documentation is also processed into searchable chunks.

The local processed data is excluded from Git using .gitignore.

Project Structure
compare_x/
│
├── app/
│   ├── api/
│   ├── comparison/
│   ├── core/
│   ├── database/
│   ├── evaluation/
│   ├── llm/
│   ├── models/
│   ├── rag/
│   ├── retrieval/
│   ├── schemas/
│   └── services/
│
├── data/
│   └── processed/
│
├── scripts/
│
├── static/
│   ├── app.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── tests/
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
Setup
1. Clone the repository
git clone <repository-url>
cd compare_x
2. Create the environment

Using Conda:

conda create -n comparex python=3.10
conda activate comparex
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Copy:

.env.example

to:

.env

Then configure:

MONGODB_URI=your_mongodb_connection_string
MONGODB_DATABASE=comparex
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
OLLAMA_MODEL=qwen3:0.6b
OLLAMA_API_BASE=http://localhost:11434

Do not commit .env.

Ollama

CompareX uses a local Qwen model through Ollama.

Make sure Ollama is installed and the required model is available.

Example:

ollama pull qwen3:0.6b

The Ollama service should be available at:

http://localhost:11434
Running CompareX

Start the FastAPI application:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

API documentation is available at:

http://127.0.0.1:8000/docs
Example Queries
Recommendation
Recommend a Samsung phone under 30000 with good camera
Battery comparison
Which smartphone has the largest battery?
Product comparison
Compare Samsung and OnePlus phones
Document question
What does the Samsung S24 manual say about battery usage?
Combined question
Recommend a Samsung smartphone and tell me about its battery.
Evaluation

The project includes lightweight evaluation and end-to-end testing.

Current validation includes:

Product retrieval              PASS
Document retrieval             PASS
Product RAG                    PASS
Document RAG                   PASS
Combined RAG                   PASS
Recommendation                 PASS
Find-best queries              PASS
Comparison queries             PASS
Frontend/API flow              PASS

The deterministic comparison evaluation currently achieves:

Accuracy: 1.00

The current retrieval evaluation verifies that retrieved products contain relevant battery information for the test query.

Limitations
The current product dataset is focused on smartphones.
Product specifications depend on the available source data.
LLM responses depend on the retrieved context.
Local Ollama inference can be slower on CPU-only systems.
The system is designed as a practical portfolio/demo application rather than a large-scale production deployment.
Future Improvements

Possible future improvements include:

Additional product categories
More brand documentation
Improved reranking
Better evaluation datasets
Additional comparison dimensions
User accounts and saved comparisons
Production deployment
More advanced document citation handling
Key Design Principle

CompareX intentionally uses a simple architecture.

Instead of introducing unnecessary agent frameworks or complex orchestration, the system separates the main responsibilities:

Query Understanding
        ↓
Product Retrieval
        ↓
Document Retrieval
        ↓
Context Construction
        ↓
LLM Generation

This keeps the system easier to understand, test, and maintain.

Project Goal

The goal of CompareX is to demonstrate how modern AI application components can be combined into a practical product recommendation and comparison system:

Structured Product Data
        +
Vector Search
        +
Document Retrieval
        +
RAG
        +
LLM
        +
FastAPI
        +
Web UI


---


## After creating it


Run:


```powershell
Get-ChildItem README.md,.env.example
