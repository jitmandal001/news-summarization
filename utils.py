import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gensim import corpora, models
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googletrans import Translator
from gtts import gTTS
import io

nltk.download('punkt')
nltk.download('stopwords')

def extract_news(company_name):
    news_sources = [
        f"https://news.google.com/search?q={company_name}&hl=en-IN&gl=IN&ceid=IN:en",
        f"https://www.reuters.com/search/news?blob={company_name}",
        f"https://www.bbc.co.uk/search?q={company_name}&page=1"
    ]
    articles = []
    
    for source in news_sources:
        response = requests.get(source)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for article in soup.find_all('article')[:4]:  # Limit to 4 articles per source
            title = article.find('h3').text if article.find('h3') else ''
            summary = article.find('p').text if article.find('p') else ''
            articles.append({'title': title, 'text': summary})
    
    return articles[:10]  # Return top 10 articles

def analyze_sentiment(text):
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']

def generate_summary(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def identify_topics(texts, num_topics=5):
    stop_words = set(stopwords.words('english'))
    texts = [[word for word in word_tokenize(text.lower()) if word not in stop_words] for text in texts]
    
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    lda_model = models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics)
    
    topics = lda_model.print_topics(num_words=3)
    return [' '.join([word for word, _ in lda_model.show_topic(topic_id, 3)]) for topic_id, _ in topics]

def text_to_speech(text, lang='hi'):
    translator = Translator()
    hindi_text = translator.translate(text, dest='hi').text
    
    tts = gTTS(text=hindi_text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    return fp
