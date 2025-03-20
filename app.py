import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import extract_news, analyze_sentiment, generate_summary, identify_topics, text_to_speech
from api import fetch_company_data

def main():
    st.title("Company News Analyzer")
    
    company_name = st.text_input("Enter company name:")
    if st.button("Analyze"):
        with st.spinner("Analyzing news..."):
            data = fetch_company_data(company_name)
            display_results(data)

def display_results(data):
    st.subheader("News Analysis Results")
    for article in data['articles']:
        st.write(f"Title: {article['title']}")
        st.write(f"Summary: {article['summary']}")
        st.write(f"Sentiment: {article['sentiment']}")
        st.write(f"Topics: {', '.join(article['topics'])}")
        st.write("---")
    
    st.subheader("Comparative Analysis")
    df = pd.DataFrame(data['articles'])
    
    # Sentiment distribution
    fig, ax = plt.subplots()
    sns.countplot(x='sentiment', data=df, ax=ax)
    st.pyplot(fig)
    
    # Topic distribution
    topics = [topic for sublist in df['topics'] for topic in sublist]
    topic_counts = pd.Series(topics).value_counts()
    fig, ax = plt.subplots()
    topic_counts.plot(kind='bar', ax=ax)
    plt.title("Top Topics")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.write(data['comparative_analysis'])
    
    st.subheader("Audio Summary (Hindi)")
    st.audio(data['audio_summary'], format='audio/wav')

if __name__ == "__main__":
    main()
