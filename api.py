from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import List, Dict, Any, Optional
import utils
import os
import json

app = FastAPI(title="News Sentiment API",
             description="API for news extraction, sentiment analysis, and text-to-speech conversion")

class CompanyRequest(BaseModel):
    company_name: str

class ArticleResponse(BaseModel):
    Title: str
    Summary: str
    Sentiment: str
    Topics: List[str]
    Source: str
    Published_Date: str
    URL: str

class ComparisonItem(BaseModel):
    Comparison: str
    Impact: str

class TopicOverlap(BaseModel):
    Common_Topics: List[str]
    Unique_Topics: List[str]

class SentimentDistribution(BaseModel):
    Positive: int
    Negative: int
    Neutral: int

class ComparativeSentiment(BaseModel):
    Sentiment_Distribution: SentimentDistribution
    Coverage_Differences: List[ComparisonItem]
    Topic_Overlap: TopicOverlap
    Final_Sentiment_Analysis: str

class CompanyResponse(BaseModel):
    Company: str
    Articles: List[ArticleResponse]
    Comparative_Sentiment_Score: ComparativeSentiment
    Final_Sentiment_Analysis: str
    Audio: str

@app.post("/api/news", response_model=CompanyResponse)
async def get_company_news(request: CompanyRequest):
    """
    Process news for a given company
    
    This endpoint extracts news articles about the specified company,
    performs sentiment analysis, and generates a comparative analysis
    along with a text-to-speech summary in Hindi.
    """
    try:
        # Process the company news
        result = utils.process_company_news(request.company_name)
        
        # Format the result to match the response model
        response = {
            "Company": result["Company"],
            "Articles": result["Articles"],
            "Comparative_Sentiment_Score": {
                "Sentiment_Distribution": result["Comparative Sentiment Score"]["Sentiment Distribution"],
                "Coverage_Differences": result["Comparative Sentiment Score"]["Coverage Differences"],
                "Topic_Overlap": {
                    "Common_Topics": result["Comparative Sentiment Score"]["Topic Overlap"]["Common Topics"],
                    "Unique_Topics": result["Comparative Sentiment Score"]["Topic Overlap"]["Unique Topics"]
                },
                "Final_Sentiment_Analysis": result["Comparative Sentiment Score"]["Final Sentiment Analysis"]
            },
            "Final_Sentiment_Analysis": result["Final Sentiment Analysis"],
            "Audio": result["Audio"]
        }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    
    Returns status of the API
    """
    return {"status": "healthy", "version": "1.0.0"}

# If executed directly, run the API server
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
