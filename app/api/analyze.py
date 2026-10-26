"""
Analyze endpoint (need.md Section 21).
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest, AnalyzeResponse
from app.services.analyzer import analyze_prompt

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_endpoint(req: QuestionRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    analysis = analyze_prompt(req.question)
    return analysis
