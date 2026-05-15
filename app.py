from fastapi import FastAPI, HTTPException
from models import ChatRequest, ChatResponse
from recommender import SHLRecommender

app = FastAPI(
    title="SHL AI Assessment Recommender",
    version="1.0.0"
)

try:
    recommender = SHLRecommender()
except Exception as e:
    recommender = None
    startup_error = str(e)


@app.get("/health")
def health():
    if recommender is None:
        return {
            "status": "error",
            "message": startup_error
        }

    return {
        "status": "ok"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if recommender is None:
        raise HTTPException(
            status_code=500,
            detail="Service initialization failed"
        )

    if not request.messages:
        raise HTTPException(
            status_code=400,
            detail="messages cannot be empty"
        )

    try:
        response = recommender.chat(request.messages)

        return ChatResponse(
            reply=response["reply"],
            recommendations=response["recommendations"],
            end_of_conversation=response["end_of_conversation"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )