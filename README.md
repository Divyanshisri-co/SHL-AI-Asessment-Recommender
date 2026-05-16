# SHL-AI-Asessment-Recommender

A conversational AI-powered recommendation system that helps recruiters and hiring teams identify suitable SHL assessments using natural language queries.

Built as part of the **SHL AI Intern Take-Home Assignment**.

---

# Project Overview

Hiring teams often struggle to identify the right assessments from large product catalogs. This project solves that by providing a conversational API that understands hiring requirements, asks clarifying questions, and recommends relevant SHL assessments from the official SHL catalog.

The system supports:

- conversational assessment discovery
- clarifying vague hiring requests
- recommending SHL assessments
- assessment comparison
- multi-turn conversation handling
- off-topic refusal
- prompt injection protection
- exact API schema compliance

The assistant only recommends assessments from SHL's official catalog dataset.

---

# Features

- SHL-only recommendations
- conversational recruiter assistant
- clarification for ambiguous requests
- assessment comparison support
- stateless API architecture
- prompt injection protection
- off-topic request refusal
- legal/compliance refusal boundaries
- semantic SHL catalog matching
- structured JSON API responses
- deployment-ready FastAPI service

---

# Tech Stack

## Backend
- FastAPI
- Uvicorn

## Programming Language
- Python 3.11+

## LLM
- Groq API
- Llama 3.3 70B Versatile

## Data Processing
- JSON
- Requests
- NumPy

## Environment
- python-dotenv

## Deployment
- Render
- GitHub

---

# System Architecture

```text
User Query
   ↓
FastAPI /chat endpoint
   ↓
Input validation
   ↓
Safety checks
   ├── vague query detection
   ├── prompt injection detection
   ├── off-topic detection
   └── legal/compliance refusal
   ↓
SHL catalog retrieval
   ↓
Context construction
   ↓
Groq LLM reasoning
   ↓
Structured JSON response
```

---

# Project Structure

```bash
shl-ai-assessment-recommender/
│
├── app.py
├── recommender.py
├── scraper.py
├── embeddings.py
├── prompts.py
├── models.py
├── requirements.txt
├── render.yaml
├── README.md
│
├── data/
│   ├── shl_catalog.json
│   ├── metadata.json
│   └── shl_index.faiss
```

---

# File Descriptions

## app.py
Main FastAPI application.

Responsibilities:
- initializes API server
- exposes `/health` endpoint
- exposes `/chat` endpoint
- validates requests
- returns assignment-compliant responses

---

## recommender.py
Core recommendation engine.

Responsibilities:
- loads SHL assessment metadata
- processes user conversations
- detects vague requests
- detects off-topic queries
- detects prompt injection attempts
- detects legal/compliance boundaries
- retrieves relevant SHL assessments
- prepares catalog context
- calls Groq LLM
- formats recommendations

---

## scraper.py
SHL catalog ingestion module.

Responsibilities:
- downloads official SHL catalog dataset
- cleans malformed JSON
- extracts structured assessment metadata
- saves processed catalog

Output:

```bash
data/shl_catalog.json
```

---

## embeddings.py
Data preparation utility.

Responsibilities:
- prepares metadata for retrieval
- structures searchable catalog records

Outputs:

```bash
data/metadata.json
data/shl_index.faiss
```

---

## prompts.py
LLM system behavior instructions.

Responsibilities:
- defines conversational rules
- restricts hallucination
- enforces SHL-only recommendations
- defines refusal behavior
- controls clarification behavior

---

## models.py
Pydantic schemas.

Responsibilities:
- request validation
- response validation
- API schema enforcement

Models:
- Message
- ChatRequest
- Recommendation
- ChatResponse

---

## requirements.txt
Python dependency list.

---

## render.yaml
Deployment configuration for Render hosting.

---

# API Endpoints

## Health Check

### GET `/health`

Checks whether the service is running.

Response:

```json
{
  "status": "ok"
}
```

---

## Chat Endpoint

### POST `/chat`

Accepts full stateless conversation history.

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a senior Java backend engineer with Spring and SQL experience"
    }
  ]
}
```

Response:

```json
{
  "reply": "Recommended SHL assessments for this role...",
  "recommendations": [
    {
      "name": "Assessment Name",
      "url": "https://www.shl.com/...",
      "test_type": "K"
    }
  ],
  "end_of_conversation": false
}
```

---

# Installation

## Clone Repository

```bash
git clone YOUR_REPOSITORY_URL
cd shl-ai-assessment-recommender
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile
```

---

# Data Preparation

Download SHL catalog:

```bash
python scraper.py
```

Prepare metadata:

```bash
python embeddings.py
```

---

# Run Locally

Start server:

```bash
uvicorn app:app --reload
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

---

# Deployment

Hosted using Render.

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
uvicorn app:app --host 0.0.0.0 --port 10000
```

## Environment Variable

```env
GROQ_API_KEY
```

---

# Example Scenarios

Supported examples:

- "Need assessment"
- "Hiring a senior Java engineer"
- "Compare OPQ and MQ"
- "Need leadership assessment for CXOs"
- "Recommend customer service assessments"
- "Hiring finance graduates"

---

# Assignment Requirements Covered

Implemented:

- conversational recommendation API
- SHL-only recommendations
- stateless conversation handling
- clarification for vague queries
- structured API responses
- comparison handling
- prompt injection protection
- off-topic refusal
- deployment-ready public endpoint
- health endpoint

---

# Future Improvements

Potential enhancements:

- stronger ranking logic
- richer role-specific recommendation rules
- language-aware recommendation refinement
- exact evaluator scenario tuning
- caching for lower latency
- smarter catalog filtering

---

# Deployment URL

Example:

```text
https://shl-ai-asessment-recommender.onrender.com
```

---

# Author

Developed for the SHL AI Intern Take-Home Assignment.
