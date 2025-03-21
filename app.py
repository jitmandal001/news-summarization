import streamlit as st
import requests
import json
import os
import base64
from typing import Dict, Any, List
import time

# Define API URL - Configure for different environments
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Set page config
st.set_page_config(
    page_title="News Sentiment Analysis",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .sentiment-positive {
        color: green;
        font-weight: bold;
    }
    .sentiment-negative {
        color: red;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: gray;
        font-weight: bold;
    }
    .article-card {
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        background-color: #f5f5f5;
    }
    .topic-tag {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        background-color: #e1e1e1;
    }
    .header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def fetch_company_news(company_name: str) -> Dict[str, Any]:
    """
    Fetch news analysis for a given company from the API
    
    Args:
        company_name: Name of the company
        
    Returns:
        Dictionary containing processed news data
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/news",
            json={"company_name": company_name},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        # For demo/testing, provide fallback sample data
        return get_sample_data(company_name)

def get_sample_data(company_name: str) -> Dict[str, Any]:
    """
    Generate sample data for demonstration when API is not available
    
    Args:
        company_name: Name of the company
        
    Returns:
        Sample data dictionary
    """
    return {
        "Company": company_name,
        "Articles": [
            {
                "Title": f"{company_name} Reports Strong Quarterly Growth",
                "Summary": f"{company_name} has reported exceptional performance in recent quarters, exceeding analyst expectations.",
                "Sentiment": "Positive",
                "Topics": ["Financial Performance", "Market Growth", "Investor Relations"],
                "Source": "Business News",
                "Published_Date": "2025-03-15",
                "URL": f"https://example.com/{company_name.lower()}/1"
            },
            {
                "Title": f"{company_name} Faces Regulatory Scrutiny",
                "Summary": f"Regulatory concerns continue to impact {company_name}'s operations and strategic plans.",
                "Sentiment": "Negative",
                "Topics": ["Regulations", "Compliance", "Legal Issues"],
                "Source": "Financial Times",
                "Published_Date": "2025-03-10",
                "URL": f"https://example.com/{company_name.lower()}/2"
            },
            {
                "Title": f"{company_name} Announces Changes to Leadership Team",
                "Summary": f"{company_name} has announced changes that could impact its operations in the coming months.",
                "Sentiment": "Neutral",
                "Topics": ["Leadership", "Corporate Governance", "Organization Structure"],
                "Source": "Market Watch",
                "Published_Date": "2025-03-05",
                "URL": f"https://example.com/{company_name.lower()}/3"
            }
        ],
        "Comparative_Sentiment_Score": {
            "Sentiment_Distribution": {
                "Positive": 1,
                "Negative": 1,
                "Neutral": 1
            },
            "Coverage_Differences": [
                {
                    "Comparison": "Positive articles focus on Financial Performance, Market Growth, while negative articles emphasize Regulations, Compliance, Legal Issues.",
                    "Impact": "This suggests a contrast in perception across different aspects of the company."
                },
                {
                    "Comparison": "Coverage varies in depth and focus across different sources.",
                    "Impact": "This highlights the importance of consulting multiple sources for a comprehensive understanding."
                }
            ],
            "Topic_Overlap": {
                "Common_Topics": ["Corporate Strategy", "Market Position"],
                "Unique_Topics": ["Financial Performance", "Regulations", "Leadership"]
            },
            "Final_Sentiment_Analysis": "Current news coverage is mixed or neutral, reflecting a complex situation."
        },
        "Final_Sentiment_Analysis": "Current news coverage is mixed or neutral, reflecting a complex situation.",
        "Audio": "sample_audio.mp3"
    }

def display_sentiment_badge(sentiment: str) -> None:
    """Display a colored badge for the sentiment"""
    if sentiment == "Positive":
        st.markdown(f'<span class="sentiment-positive">Positive</span>', unsafe_allow_html=True)
    elif sentiment == "Negative":
        st.markdown(f'<span class="sentiment-negative">Negative</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="sentiment-neutral">Neutral</span>', unsafe_allow_html=True)

def display_topics(topics: List[str]) -> None:
    """Display topic tags"""
    html = ""
    for topic in topics:
        html += f'<span class="topic-tag">{topic}</span>'
    st.markdown(html, unsafe_allow_html=True)

def display_article_card(article: Dict[str, Any], index: int) -> None:
    """Display an article in a card format"""
    with st.container():
        st.markdown(f'<div class="article-card">', unsafe_allow_html=True)
        
        # Title and sentiment
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {article['Title']}")
        with col2:
            st.markdown("**Sentiment:**")
            display_sentiment_badge(article['Sentiment'])
        
        # Summary
        st.markdown("**Summary:**")
        st.write(article['Summary'])
        
        # Topics
        st.markdown("**Topics:**")
        display_topics(article['Topics'])
        
        # Source and date
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Source:** {article['Source']}")
        with col2:
            st.markdown(f"**Published:** {article['Published_Date']}")
        
        # URL
        st.markdown(f"[Read full article]({article['URL']})")
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_comparative_analysis(analysis: Dict[str, Any]) -> None:
    """Display the comparative analysis section"""
    st.subheader("Sentiment Distribution")
    
    # Display sentiment distribution as a bar chart
    sentiments = analysis["Sentiment_Distribution"]
    st.bar_chart(sentiments)
    
    # Coverage differences
    st.subheader("Coverage Analysis")
    for item in analysis["Coverage_Differences"]:
        st.markdown(f"**Observation:** {item['Comparison']}")
        st.markdown(f"*Impact:* {item['Impact']}")
        st.markdown("---")
    
    # Topic overlap
    st.subheader("Topic Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Common Topics Across Articles:**")
        for topic in analysis["Topic_Overlap"]["Common_Topics"]:
            st.markdown(f"- {topic}")
    
    with col2:
        st.markdown("**Unique Topics:**")
        for topic in analysis["Topic_Overlap"]["Unique_Topics"]:
            st.markdown(f"- {topic}")
    
    # Final sentiment
    st.subheader("Overall Sentiment Analysis")
    st.info(analysis["Final_Sentiment_Analysis"])

def main():
    st.title("📰 Company News Sentiment Analysis")
    st.markdown("""
    This application extracts key details from news articles related to a given company, 
    performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech 
    output in Hindi.
    """)
    
    # Company selection
    st.header("Enter Company Name")
    
    # Example companies for dropdown
    example_companies = [
        "Tesla",
        "Apple",
        "Google",
        "Microsoft",
        "Amazon",
        "Facebook",
        "Netflix",
        "Other (specify)"
    ]
    
    company_option = st.selectbox(
        "Select a company or choose 'Other' to specify:",
        example_companies
    )
    
    company_name = ""
    if company_option == "Other (specify)":
        company_name = st.text_input("Enter company name:")
    else:
        company_name = company_option
    
    # Process button
    if st.button("Analyze News") and company_name:
        with st.spinner(f"Analyzing news for {company_name}..."):
            # Display a progress bar to show work is happening
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)  # Simulate work
                progress_bar.progress(i + 1)
            
            # Fetch data from API
            result = fetch_company_news(company_name)
            
            if result:
                # Display results
                st.header(f"News Analysis for {result['Company']}")
                
                # Summary tabs
                tab1, tab2, tab3 = st.tabs(["Articles", "Comparative Analysis", "Audio Summary"])
                
                with tab1:
                    st.subheader("Articles Analysis")
                    for i, article in enumerate(result["Articles"]):
                        display_article_card(article, i)
                
                with tab2:
                    st.subheader("Comparative Sentiment Analysis")
                    display_comparative_analysis(result["Comparative_Sentiment_Score"])
                
                with tab3:
                    st.subheader("Audio Summary (Hindi)")
                    st.markdown("Listen to the audio summary of the news analysis in Hindi:")
                    
                    # In a real implementation, you would provide the actual audio file
                    # For demonstration, we'll show a placeholder
                    st.audio("https://upload.wikimedia.org/wikipedia/commons/5/5b/Hindi_svar.ogg", format="audio/ogg")
                    
                    st.markdown("**Note:** This is a placeholder audio. In the actual implementation, the audio would be a Hindi text-to-speech conversion of the news summary.")
    
    # Information section
    st.sidebar.title("About")
    st.sidebar.info("""
    This application performs news extraction, sentiment analysis, and text-to-speech conversion
    for company news articles.
    
    **Features:**
    - Extract news from multiple sources
    - Analyze sentiment (positive, negative, neutral)
    - Identify key topics in articles
    - Compare sentiment across articles
    - Generate Hindi audio summary
    
    **Technologies Used:**
    - Natural Language Processing
    - Sentiment Analysis
    - Text-to-Speech Conversion
    - Web Scraping
    """)
    
    st.sidebar.title("Instructions")
    st.sidebar.markdown("""
    1. Select a company from the dropdown or enter a custom company name
    2. Click "Analyze News" to start the analysis
    3. View the results in the three tabs:
       - Articles: Individual article analysis
       - Comparative Analysis: Cross-article insights
       - Audio Summary: Hindi speech summary
    """)

if __name__ == "__main__":
    main()
