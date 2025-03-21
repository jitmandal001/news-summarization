import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import nltk
import spacy
from collections import Counter
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os
import json
from typing import List, Dict, Any, Tuple
import time
import random

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load spaCy model for topic extraction
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Download if not available
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Initialize text summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_news_articles(company_name: str, num_articles: int = 10) -> List[Dict[str, Any]]:
    """
    Extract news articles related to a given company.
    
    Args:
        company_name: Name of the company to search for
        num_articles: Number of articles to extract (default: 10)
        
    Returns:
        List of dictionaries containing article details
    """
    articles = []
    
    # Create search query
    query = f"{company_name} news"
    
    # We'll simulate getting articles from multiple sources
    sources = [
        f"https://www.google.com/search?q={query}&tbm=nws",
        f"https://news.search.yahoo.com/search?p={query}",
        f"https://www.bing.com/news/search?q={query}"
    ]
    
    # For demonstration purposes, I'll create a function to simulate article extraction
    # In a real implementation, you would use BeautifulSoup to parse the actual HTML
    
    for source in sources:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(source, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # The actual parsing would depend on the specific website structure
                # For demonstration, I'll create a simulation
                
                # Simulate finding articles
                article_elements = simulate_article_elements(company_name, min(5, num_articles - len(articles)))
                
                for article in article_elements:
                    if len(articles) < num_articles:
                        articles.append(article)
                    else:
                        break
            
            if len(articles) >= num_articles:
                break
                
        except Exception as e:
            print(f"Error extracting from {source}: {e}")
    
    # Ensure we have exactly num_articles articles
    while len(articles) < num_articles:
        articles.append(simulate_article(company_name, len(articles) + 1))
    
    return articles[:10]

def simulate_article_elements(company_name: str, count: int) -> List[Dict[str, Any]]:
    """Simulate article extraction for demonstration purposes"""
    articles = []
    
    topics = [
        ["Finance", "Stock Market", "Investment"],
        ["Technology", "Innovation", "Digital Transformation"],
        ["Business", "Strategy", "Market Growth"],
        ["Leadership", "Management", "Corporate Governance"],
        ["Products", "Services", "Customer Experience"],
        ["Competition", "Market Share", "Industry Trends"],
        ["Sustainability", "ESG", "Corporate Responsibility"],
        ["Regulations", "Compliance", "Legal Issues"],
        ["Employees", "Workplace", "Corporate Culture"],
        ["International", "Global Market", "Expansion"]
    ]
    
    for i in range(count):
        # Generate a random sentiment tendency for variety
        sentiment_tendency = random.choice(["positive", "negative", "neutral"])
        
        # Create a random title based on sentiment
        if sentiment_tendency == "positive":
            title_templates = [
                f"{company_name} Reports Strong Quarterly Growth",
                f"{company_name} Launches Innovative New Product",
                f"{company_name} Expands into New Markets",
                f"Investors Optimistic About {company_name}'s Future",
                f"{company_name} Partners with Industry Leader"
            ]
        elif sentiment_tendency == "negative":
            title_templates = [
                f"{company_name} Faces Regulatory Scrutiny",
                f"{company_name} Stock Drops Amid Market Concerns",
                f"Challenges Ahead for {company_name}",
                f"Critics Question {company_name}'s Business Strategy",
                f"{company_name} Struggles with Supply Chain Issues"
            ]
        else:
            title_templates = [
                f"{company_name} Announces Changes to Leadership Team",
                f"{company_name} Releases Quarterly Report",
                f"Analysis: {company_name}'s Position in the Market",
                f"{company_name} Updates Corporate Policies",
                f"Industry Report Includes {company_name}"
            ]
            
        title = random.choice(title_templates)
        
        # Create content based on sentiment and title
        selected_topics = random.choice(topics)
        content = generate_article_content(company_name, title, sentiment_tendency, selected_topics)
        
        article = {
            "title": title,
            "content": content,
            "url": f"https://news.example.com/{company_name.lower().replace(' ', '-')}/{i+1}",
            "published_date": simulate_date(),
            "source": random.choice(["Business News", "Tech Today", "Financial Times", "Market Watch", "Industry Insider"])
        }
        
        articles.append(article)
    
    return articles

def simulate_article(company_name: str, index: int) -> Dict[str, Any]:
    """Create a simulated article for demonstration purposes"""
    return simulate_article_elements(company_name, 1)[0]

def simulate_date() -> str:
    """Generate a random recent date"""
    today = pd.Timestamp.now()
    days_ago = random.randint(1, 30)
    date = today - pd.Timedelta(days=days_ago)
    return date.strftime("%Y-%m-%d")

def generate_article_content(company_name: str, title: str, sentiment: str, topics: List[str]) -> str:
    """Generate article content for demonstration purposes"""
    # Base templates for different sentiment types
    positive_templates = [
        f"{company_name} has reported exceptional performance in recent quarters, exceeding analyst expectations.",
        f"Investors are showing increased confidence in {company_name}'s long-term growth strategy.",
        f"The innovative approach taken by {company_name} has positioned it ahead of competitors in the market.",
        f"Industry experts praise {company_name}'s commitment to quality and customer satisfaction.",
        f"The recent initiatives launched by {company_name} have been well-received by stakeholders."
    ]
    
    negative_templates = [
        f"{company_name} faces significant challenges in the current market environment.",
        f"Regulatory concerns continue to impact {company_name}'s operations and strategic plans.",
        f"Analysts express caution regarding {company_name}'s recent business decisions.",
        f"Competition has intensified, putting pressure on {company_name}'s market position.",
        f"Shareholders have raised questions about {company_name}'s current direction and leadership."
    ]
    
    neutral_templates = [
        f"{company_name} has announced changes that could impact its operations in the coming months.",
        f"Market analysts are closely monitoring {company_name}'s performance in the evolving industry landscape.",
        f"The recent developments at {company_name} reflect broader trends in the sector.",
        f"Industry reports include {company_name} among companies adapting to new market conditions.",
        f"Experts suggest {company_name}'s strategy aligns with typical patterns in the industry."
    ]
    
    # Select templates based on sentiment
    if sentiment == "positive":
        templates = positive_templates
    elif sentiment == "negative":
        templates = negative_templates
    else:
        templates = neutral_templates
    
    # Generate paragraphs
    num_paragraphs = random.randint(4, 8)
    paragraphs = []
    
    # First paragraph often introduces the article topic
    first_para = f"In recent news about {company_name}, {random.choice(templates).lower()} "
    first_para += f"This development comes as the company continues to navigate the challenges and opportunities in the {topics[0].lower()} sector. "
    first_para += f"Industry watchers note that {company_name}'s approach to {topics[1].lower()} has been a defining factor in its recent performance."
    paragraphs.append(first_para)
    
    # Generate middle paragraphs
    for i in range(1, num_paragraphs - 1):
        para = random.choice(templates) + " "
        para += f"This is particularly relevant in the context of {topics[random.randint(0, len(topics)-1)].lower()}. "
        para += f"Market analysts point out that {company_name}'s strategy in this area could have significant implications for its future growth and competitive positioning."
        paragraphs.append(para)
    
    # Last paragraph often contains forward-looking statements or conclusions
    last_para = f"Looking ahead, {company_name} is expected to continue focusing on its core strengths in {topics[random.randint(0, len(topics)-1)].lower()}. "
    last_para += f"The company's approach to {topics[random.randint(0, len(topics)-1)].lower()} will likely remain a key factor in its market performance. "
    last_para += f"Stakeholders will be watching closely as {company_name} navigates the evolving landscape in the coming months."
    paragraphs.append(last_para)
    
    return "\n\n".join(paragraphs)

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of the given text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary containing sentiment analysis results
    """
    # For longer texts, we'll analyze sentences and aggregate
    if len(text) > 512:
        sentences = sent_tokenize(text)
        
        # Analyze each sentence
        results = []
        for sentence in sentences:
            if len(sentence.strip()) > 10:  # Skip very short sentences
                try:
                    result = sentiment_analyzer(sentence)[0]
                    results.append(result)
                except Exception as e:
                    print(f"Error analyzing sentence: {e}")
        
        # Count positive, negative, neutral sentiments
        positive_count = sum(1 for r in results if r['label'] == 'POSITIVE')
        negative_count = sum(1 for r in results if r['label'] == 'NEGATIVE')
        
        # Calculate overall sentiment
        if positive_count > negative_count * 1.5:
            overall_sentiment = "Positive"
        elif negative_count > positive_count * 1.5:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"
            
        # Calculate confidence
        confidence = sum(r['score'] for r in results) / len(results) if results else 0.5
        
        return {
            "sentiment": overall_sentiment,
            "confidence": confidence,
            "details": {
                "positive_sentences": positive_count,
                "negative_sentences": negative_count,
                "neutral_sentences": len(results) - positive_count - negative_count
            }
        }
    else:
        # For shorter texts, analyze directly
        try:
            result = sentiment_analyzer(text)[0]
            sentiment = "Positive" if result['label'] == 'POSITIVE' else "Negative"
            return {
                "sentiment": sentiment,
                "confidence": result['score'],
                "details": {
                    "positive_sentences": 1 if sentiment == "Positive" else 0,
                    "negative_sentences": 1 if sentiment == "Negative" else 0,
                    "neutral_sentences": 0
                }
            }
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return {
                "sentiment": "Neutral",
                "confidence": 0.5,
                "details": {
                    "positive_sentences": 0,
                    "negative_sentences": 0,
                    "neutral_sentences": 1
                }
            }

def extract_topics(text: str, num_topics: int = 3) -> List[str]:
    """
    Extract key topics from the text.
    
    Args:
        text: Text to analyze
        num_topics: Number of topics to extract
        
    Returns:
        List of topics
    """
    # Parse text with spaCy
    doc = nlp(text)
    
    # Extract noun phrases and named entities
    noun_phrases = []
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:  # Limit to phrases with 3 or fewer words
            noun_phrases.append(chunk.text.lower())
    
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW"]:
            entities.append(ent.text.lower())
    
    # Count occurrences
    phrase_counts = Counter(noun_phrases)
    entity_counts = Counter(entities)
    
    # Combine and get most common
    all_topics = phrase_counts + entity_counts
    
    # Filter out single words and very common words
    filtered_topics = [(topic, count) for topic, count in all_topics.items() 
                      if len(topic.split()) > 1 or (len(topic) > 4 and topic not in ["news", "report", "company", "business"])]
    
    # Get top topics
    top_topics = [topic for topic, _ in sorted(filtered_topics, key=lambda x: x[1], reverse=True)[:num_topics*2]]
    
    # For demonstration, ensure we have at least some topics
    if not top_topics or len(top_topics) < num_topics:
        default_topics = ["Business Strategy", "Market Growth", "Financial Performance", 
                         "Product Development", "Industry Trends", "Competitive Analysis"]
        top_topics.extend(default_topics)
        top_topics = list(set(top_topics))  # Remove duplicates
    
    # Capitalize each word in the topics
    formatted_topics = [' '.join(word.capitalize() for word in topic.split()) for topic in top_topics[:num_topics]]
    
    return formatted_topics

def generate_summary(text: str, max_length: int = 150) -> str:
    """
    Generate a summary of the text.
    
    Args:
        text: Text to summarize
        max_length: Maximum length of the summary
        
    Returns:
        Summary text
    """
    # For demonstration, we'll use a simple approach
    # In a real implementation, you would use a more sophisticated model
    
    # Check if text is short enough already
    if len(text) <= max_length:
        return text
    
    try:
        # Use transformers summarization pipeline
        summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        
        # Fallback: extract first few sentences
        sentences = sent_tokenize(text)
        summary = ""
        for sentence in sentences:
            if len(summary) + len(sentence) <= max_length:
                summary += sentence + " "
            else:
                break
        
        return summary.strip()

def perform_comparative_analysis(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Perform comparative analysis across articles.
    
    Args:
        articles: List of article dictionaries with sentiment and topics
        
    Returns:
        Dictionary containing comparative analysis results
    """
    # Count sentiments
    sentiment_counts = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }
    
    for article in articles:
        sentiment = article.get("Sentiment", "Neutral")
        sentiment_counts[sentiment] += 1
    
    # Collect all topics
    all_topics = []
    for article in articles:
        all_topics.extend(article.get("Topics", []))
    
    # Count topic frequency
    topic_counts = Counter(all_topics)
    common_topics = [topic for topic, count in topic_counts.most_common(5)]
    
    # Generate comparisons
    comparisons = []
    
    # Compare positive vs negative articles
    if sentiment_counts["Positive"] > 0 and sentiment_counts["Negative"] > 0:
        positive_articles = [a for a in articles if a.get("Sentiment") == "Positive"]
        negative_articles = [a for a in articles if a.get("Sentiment") == "Negative"]
        
        pos_topics = []
        for article in positive_articles:
            pos_topics.extend(article.get("Topics", []))
        
        neg_topics = []
        for article in negative_articles:
            neg_topics.extend(article.get("Topics", []))
            
        pos_topic_counts = Counter(pos_topics)
        neg_topic_counts = Counter(neg_topics)
        
        pos_focus = [topic for topic, _ in pos_topic_counts.most_common(3)]
        neg_focus = [topic for topic, _ in neg_topic_counts.most_common(3)]
        
        comparisons.append({
            "Comparison": f"Positive articles focus on {', '.join(pos_focus)}, while negative articles emphasize {', '.join(neg_focus)}.",
            "Impact": "This suggests a contrast in perception across different aspects of the company."
        })
    
    # Check for topic variation
    if common_topics:
        unique_topics = [topic for topic, count in topic_counts.items() if count == 1]
        if unique_topics:
            comparisons.append({
                "Comparison": f"While {', '.join(common_topics[:3])} are common themes, some articles uniquely cover {', '.join(unique_topics[:3])}.",
                "Impact": "This indicates a diversity in media coverage, exploring various aspects of the company."
            })
    
    # Overall sentiment trend
    if sentiment_counts["Positive"] > sentiment_counts["Negative"] + sentiment_counts["Neutral"]:
        sentiment_trend = "overwhelmingly positive"
    elif sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        sentiment_trend = "generally positive"
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"] + sentiment_counts["Neutral"]:
        sentiment_trend = "overwhelmingly negative"
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        sentiment_trend = "generally negative"
    else:
        sentiment_trend = "mixed or neutral"
    
    comparisons.append({
        "Comparison": f"The overall sentiment across articles is {sentiment_trend}.",
        "Impact": f"This suggests that current media coverage is {sentiment_trend}, which may influence public and investor perception."
    })
    
    # Ensure we have at least 3 comparisons
    if len(comparisons) < 3:
        comparisons.append({
            "Comparison": "Coverage varies in depth and focus across different sources.",
            "Impact": "This highlights the importance of consulting multiple sources for a comprehensive understanding."
        })
    
    # Create topic overlap analysis
    topic_overlap = {
        "Common Topics": common_topics[:3] if common_topics else [],
        "Unique Topics": unique_topics[:5] if 'unique_topics' in locals() and unique_topics else []
    }
    
    # Calculate final sentiment
    final_sentiment = ""
    if sentiment_counts["Positive"] > sentiment_counts["Negative"] + sentiment_counts["Neutral"]:
        final_sentiment = "overwhelmingly positive, suggesting strong performance and optimistic outlook"
    elif sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        final_sentiment = "generally positive, with some areas of concern"
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"] + sentiment_counts["Neutral"]:
        final_sentiment = "predominantly negative, indicating significant challenges"
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        final_sentiment = "somewhat negative, with some positive aspects"
    else:
        final_sentiment = "mixed or neutral, reflecting a complex situation"
    
    return {
        "Sentiment Distribution": sentiment_counts,
        "Coverage Differences": comparisons,
        "Topic Overlap": topic_overlap,
        "Final Sentiment Analysis": f"Current news coverage is {final_sentiment}."
    }

from gtts import gTTS
import os

def convert_text_to_hindi_speech(text: str, output_filename: str = "output.mp3") -> str:
    """
    Convert text to Hindi speech and save as an MP3 file.
    
    Args:
        text: The text to convert to speech (in Hindi).
        output_filename: The name of the output MP3 file.
    
    Returns:
        The path to the saved MP3 file.
    """
    try:
        # Create a gTTS object with Hindi language
        tts = gTTS(text=text, lang='hi', slow=False)
        
        # Save the audio file
        tts.save(output_filename)
        
        # Get the absolute path of the saved file
        file_path = os.path.abspath(output_filename)
        
        return file_path
    except Exception as e:
        print(f"Error converting text to speech: {str(e)}")
        return ""

   
