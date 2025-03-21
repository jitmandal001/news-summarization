from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import extract_news, analyze_sentiment, generate_summary, identify_topics, text_to_speech

app = FastAPI()

class CompanyRequest(BaseModel):
    name: str

@app.post("/analyze_company")
async def analyze_company(request: CompanyRequest):
    try:
        articles = extract_news(request.name)
        results = []
        all_texts = []
        for article in articles:
            sentiment, score = analyze_sentiment(article['text'])
            summary = generate_summary(article['text'])
            all_texts.append(article['text'])
            results.append({
                'Title': article['title'],
                'Summary': summary,
                'Sentiment': sentiment,
                'Topics': identify_topics([article['text']])
            })

        sentiment_distribution = {
            "Positive": len([r for r in results if r['Sentiment'] == 'POSITIVE']),
            "Negative": len([r for r in results if r['Sentiment'] == 'NEGATIVE']),
            "Neutral": len([r for r in results if r['Sentiment'] == 'NEUTRAL'])
        }

        coverage_differences = [
            {
                "Comparison": "Comparison text between articles...",
                "Impact": "Analysis of impact..."
            }
        ]

        topic_overlap = {
            "Common Topics": list(set.intersection(*[set(r['Topics']) for r in results])),
            "Unique Topics": {f"Article {i+1}": list(set(r['Topics']) - set.union(*[set(res['Topics']) for j, res in enumerate(results) if j != i])) for i, r in enumerate(results)}
        }

        final_sentiment = max(sentiment_distribution, key=sentiment_distribution.get)
        final_analysis = f"The overall sentiment towards {request.name} is {final_sentiment.lower()}."

        audio_summary = text_to_speech(final_analysis)

        return {
            "Company": request.name,
            "Articles": results,
            "Comparative Sentiment Score": {
                "Sentiment Distribution": sentiment_distribution,
                "Coverage Differences": coverage_differences,
                "Topic Overlap": topic_overlap
            },
            "Final Sentiment Analysis": final_analysis,
            "Audio": "[Play Hindi Speech]"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
