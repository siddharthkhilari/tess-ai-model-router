"""
Generate endpoint (need.md Section 21).
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest, GenerateResponse, CompareRequest, CompareResponse
from app.services.inference import process_inference_request, run_model_comparison

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
def generate_endpoint(req: QuestionRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        result = process_inference_request(req.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference processing failed: {str(e)}")

@router.post("/compare", response_model=CompareResponse)
def compare_endpoint(req: CompareRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        result = run_model_comparison(req.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
