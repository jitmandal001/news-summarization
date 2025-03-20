---
title: News Summarization
emoji: 👍
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: "1.43.2"
app_file: app.py
pinned: false
---
# News Summarization and Text-to-Speech Application

This application extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.

## Objective

Develop a web-based application that allows users to input a company name and receive a structured sentiment report along with an audio output.

## Requirements

1. **News Extraction**: Extract and display the title, summary, and other relevant metadata from at least 10 unique news articles related to the given company using BeautifulSoup (bs4).
2. **Sentiment Analysis**: Perform sentiment analysis on the article content (positive, negative, neutral).
3. **Comparative Analysis**: Conduct a comparative sentiment analysis across the articles to derive insights on how the company's news coverage varies.
4. **Text-to-Speech**: Convert the summarized content into Hindi speech using an open-source TTS model.
5. **User Interface**: Provide a simple web-based interface using Streamlit where users can input a company name to fetch news articles and generate the sentiment report.
6. **API Development**: Communication between the frontend and backend must happen via APIs.
7. **Deployment**: Deploy the application on Hugging Face Spaces for testing.
8. **Documentation**: Submit a detailed README file explaining implementation, dependencies, and setup instructions.