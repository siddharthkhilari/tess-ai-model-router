"""
Pydantic schemas for API request and response validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000, description="User question or prompt")

class PrivacyAnalysis(BaseModel):
    level: str
    matched_keywords: List[str]
    routing_note: str

class ScoreBreakdown(BaseModel):
    length_score: int
    instruction_score: int
    reasoning_score: int
    technical_score: int
    task_score: int

class AnalyzeResponse(BaseModel):
    question: str
    word_count: int
    char_count: int
    sentence_count: int = 1
    score: int
    complexity_level: str
    breakdown: Optional[ScoreBreakdown] = None
    reasons: List[str]

class GenerateResponse(BaseModel):
    question: str
    response: str
    selected_model: str
    selected_model_name: str
    complexity_level: str
    complexity_score: float
    privacy_level: str
    latency_ms: float
    estimated_cost: float
    baseline_cost: float
    estimated_saving: float
    estimated_saving_pct: float
    cache_hit: bool
    routing_reason: str
    reasons: List[str]

class ModelInfo(BaseModel):
    id: str
    name: str
    tier: str
    description: str
    estimated_cost: float
    expected_quality: int
    expected_latency: float
    available: bool

class CompareRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)

class ModelComparisonItem(BaseModel):
    model_id: str
    model_name: str
    tier: str
    expected_quality: int
    estimated_cost: float
    expected_latency: float
    actual_latency_ms: float
    response: str
    is_recommended: bool

class CompareResponse(BaseModel):
    question: str
    recommended_model: str
    recommendation_reason: str
    models: List[ModelComparisonItem]

class DashboardStats(BaseModel):
    total_requests: int
    average_latency_ms: float
    estimated_total_cost: float
    estimated_total_savings: float
    overall_saving_percentage: float
    cache_hit_rate: float
    model_usage: Dict[str, int]
    model_usage_percentage: Dict[str, float]
    complexity_distribution: Dict[str, int]
    timeline: List[Dict[str, Any]]
