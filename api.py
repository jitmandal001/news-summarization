from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import extract_news, analyze_sentiment, generate_summary, identify_topics, text_to_speech

app = FastAPI()

class CompanyRequest(BaseModel):
    name: str
# hosted on hugging face
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
                'title': article['title'],
                'summary': summary,
                'sentiment': sentiment,
                'sentiment_score': score,
            })
        
        topics = identify_topics(all_texts)
        for result, topic in zip(results, topics):
            result['topics'] = topic.split()
        
        comparative_analysis = perform_comparative_analysis(results)
        overall_summary = generate_overall_summary(results)
        audio_summary = text_to_speech(overall_summary)
        
        return {
            'articles': results,
            'comparative_analysis': comparative_analysis,
            'audio_summary': audio_summary.getvalue()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def perform_comparative_analysis(results):
    sentiments = [result['sentiment'] for result in results]
    positive = sentiments.count('POSITIVE')
    negative = sentiments.count('NEGATIVE')
    neutral = sentiments.count('NEUTRAL')
    
    return f"Comparative Analysis: {positive} positive, {negative} negative, and {neutral} neutral articles."

def generate_overall_summary(results):
    overall_sentiment = max(set([result['sentiment'] for result in results]), key=[result['sentiment'] for result in results].count)
    top_topics = set([topic for result in results for topic in result['topics']])
    
    return f"Overall sentiment is {overall_sentiment}. Top topics include {', '.join(list(top_topics)[:5])}."
