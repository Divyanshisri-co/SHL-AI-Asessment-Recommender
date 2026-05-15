# SHL-AI-Asessment-Recommender

A conversational AI recommendation system that helps recruiters and hiring managers discover appropriate SHL assessments through natural language interaction.

Built for the **SHL AI Intern Take-Home Assignment**.

---

## Project Overview

Traditional assessment catalogs require users to already know what they are searching for. This project solves that problem by building a conversational AI agent that understands hiring requirements, asks clarifying questions when needed, and recommends relevant SHL assessments from the official SHL product catalog.

The assistant is designed to:

- Understand vague hiring requirements
- Ask clarifying questions before recommending
- Recommend relevant SHL assessments
- Compare assessments when requested
- Handle changing requirements during conversation
- Refuse unrelated or unsafe requests
- Return structured responses in the exact required API schema

This implementation uses the **official SHL assessment catalog dataset provided in the assignment**.

---

## Features

- Conversational assessment recommendation
- Semantic search over SHL assessment catalog
- SHL-only grounded recommendations
- Clarification for vague user requests
- Comparison between assessments
- Refinement support during multi-turn conversations
- Stateless API design
- Prompt injection protection
- Off-topic refusal handling
- Fast API response architecture
- Deployment-ready setup

---

## Tech Stack

### Backend Framework
- FastAPI
- Uvicorn

### Programming Language
- Python 3.11+

### LLM
- Groq API
- Llama 3.3 70B Versatile

### Embedding Model
- Sentence Transformers
- all-MiniLM-L6-v2

### Vector Search
- FAISS

### Data Handling
- Requests
- JSON
- NumPy

### Environment Management
- python-dotenv

### Deployment
- Render
- GitHub

---

## System Architecture

User Query
↓
FastAPI `/chat`
↓
Conversation preprocessing
↓
Safety checks
- vague query detection
- off-topic detection
- prompt injection detection
↓
Semantic retrieval using FAISS
↓
Relevant SHL assessments retrieved
↓
Context sent to Groq LLM
↓
Structured response returned

---

## API Endpoints

### 1. Health Check

**GET /health**

Checks service readiness.

Example:

```json
{
  "status": "ok"
}
```

---

### 2. Chat Endpoint

**POST /chat**

Accepts full stateless conversation history.

Example Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a mid-level Java developer with stakeholder communication skills"
    }
  ]
}
```

Example Response:

```json
{
  "reply": "Here are relevant SHL assessments for this role.",
  "recommendations": [
    {
      "name": "Java Assessment",
      "url": "https://www.shl.com/...",
      "test_type": "K"
    }
  ],
  "end_of_conversation": true
}
```

---

## Project Structure

```bash
shl-ai-assessment-recommender/
│
├── app.py
├── recommender.py
├── scraper.py
├── embeddings.py
├── models.py
├── prompts.py
├── requirements.txt
├── render.yaml
├── README.md
├── .gitignore
│
├── data/
│   ├── shl_catalog.json
│   ├── metadata.json
│   └── shl_index.faiss
```

---

## File Descriptions

### app.py
Main FastAPI application.

Responsibilities:
- Starts API server
- Exposes `/health` endpoint
- Exposes `/chat` endpoint
- Validates incoming requests
- Returns structured assignment-compliant responses

---

### recommender.py
Core recommendation engine.

Responsibilities:
- Loads vector search index
- Loads SHL metadata
- Handles conversation history
- Detects vague queries
- Detects off-topic queries
- Detects prompt injection attempts
- Retrieves relevant assessments
- Sends grounded context to Groq LLM
- Formats recommendations

---

### scraper.py
Catalog ingestion module.

Responsibilities:
- Downloads official SHL assessment catalog dataset
- Cleans malformed JSON
- Extracts assessment metadata
- Maps dataset into internal project schema

Generated output:

```bash
data/shl_catalog.json
```

---

### embeddings.py
Vector search preparation module.

Responsibilities:
- Loads assessment catalog
- Builds searchable documents
- Generates embeddings
- Creates FAISS vector index
- Saves metadata

Generated outputs:

```bash
data/shl_index.faiss
data/metadata.json
```

---

### models.py
Pydantic data models.

Responsibilities:
- Request validation
- Response validation
- Assignment schema enforcement

Includes:
- Message
- ChatRequest
- Recommendation
- ChatResponse

---

### prompts.py
System instruction module.

Responsibilities:
- Defines LLM behavior
- Restricts hallucinations
- Enforces SHL-only recommendations
- Controls refusal behavior
- Defines conversational rules

---

### requirements.txt
Dependency list for Python environment.

---

### render.yaml
Deployment configuration for Render.

Responsibilities:
- Dependency installation
- Data preparation
- Server startup

---

## Installation Guide

### 1. Clone Repository

```bash
git clone YOUR_REPOSITORY_URL
cd shl-ai-assessment-recommender
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

---

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile
```

---

## Data Preparation

Download SHL catalog:

```bash
python scraper.py
```

Expected:

```bash
Saved 377 assessments
```

Generate embeddings:

```bash
python embeddings.py
```

---

## Run Locally

Start server:

```bash
uvicorn app:app --reload
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

---

## Deployment (Render)

### Build Command

```bash
pip install -r requirements.txt && python scraper.py && python embeddings.py
```

### Start Command

```bash
uvicorn app:app --host 0.0.0.0 --port 10000
```

### Environment Variables

Add:

```env
GROQ_API_KEY
```

---

## Example Test Cases

### Vague Query

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need assessment"
    }
  ]
}
```

Expected behavior:
- asks clarification
- returns empty recommendations

---

### Specific Hiring Request

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer with stakeholder communication skills"
    }
  ]
}
```

Expected behavior:
- recommends relevant SHL assessments

---

### Comparison Query

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Compare OPQ and MQ"
    }
  ]
}
```

Expected behavior:
- grounded comparison
- no hallucinated recommendations

---

## Assignment Requirements Covered

Implemented:

- SHL-only recommendations
- Full conversation history support
- Stateless API architecture
- Clarification for vague queries
- Recommendation generation
- Assessment comparison
- Requirement refinement
- Off-topic refusal
- Prompt injection resistance
- Health endpoint
- Exact response schema compliance

---

## Future Improvements

Potential enhancements:

- Better recommendation ranking
- More accurate assessment comparison
- Retrieval filtering improvements
- Response caching
- Evaluation benchmark automation
- Faster inference optimization

---

## Author

Developed for the SHL AI Intern Take-Home Assignment.
