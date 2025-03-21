# # import streamlit as st
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # import seaborn as sns
# # from utils import extract_news, analyze_sentiment, generate_summary, identify_topics, text_to_speech
# # from api import fetch_company_data

# # def main():
# #     st.title("Company News Analyzer")
    
# #     company_name = st.text_input("Enter company name:")
# #     if st.button("Analyze"):
# #         with st.spinner("Analyzing news..."):
# #             data = fetch_company_data(company_name)
# #             display_results(data)

# # def display_results(data):
# #     st.subheader("News Analysis Results")
# #     for article in data['articles']:
# #         st.write(f"Title: {article['title']}")
# #         st.write(f"Summary: {article['summary']}")
# #         st.write(f"Sentiment: {article['sentiment']}")
# #         st.write(f"Topics: {', '.join(article['topics'])}")
# #         st.write("---")
    
# #     st.subheader("Comparative Analysis")
# #     df = pd.DataFrame(data['articles'])
    
# #     # Sentiment distribution
# #     fig, ax = plt.subplots()
# #     sns.countplot(x='sentiment', data=df, ax=ax)
# #     st.pyplot(fig)
    
# #     # Topic distribution
# #     topics = [topic for sublist in df['topics'] for topic in sublist]
# #     topic_counts = pd.Series(topics).value_counts()
# #     fig, ax = plt.subplots()
# #     topic_counts.plot(kind='bar', ax=ax)
# #     plt.title("Top Topics")
# #     plt.xticks(rotation=45)
# #     st.pyplot(fig)
    
# #     st.write(data['comparative_analysis'])
    
# #     st.subheader("Audio Summary (Hindi)")
# #     st.audio(data['audio_summary'], format='audio/wav')

# # if __name__ == "__main__":
# #     main()
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from api import fetch_company_data

# def main():
#     st.title("Company News Analyzer")
#     company_name = st.text_input("Enter company name:")

#     if st.button("Analyze"):
#         with st.spinner("Analyzing news..."):
#             try:
#                 data = fetch_company_data(company_name)
#                 display_results(data)
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")

# def display_results(data):
#     st.subheader("News Analysis Results")
#     for article in data['Articles']:
#         st.write(f"Title: {article['Title']}")
#         st.write(f"Summary: {article['Summary']}")
#         st.write(f"Sentiment: {article['Sentiment']}")
#         st.write(f"Topics: {', '.join(article['Topics'])}")
#         st.write("---")

#     st.subheader("Comparative Analysis")
#     sentiment_dist = data['Comparative Sentiment Score']['Sentiment Distribution']
#     df = pd.DataFrame.from_dict(sentiment_dist, orient='index', columns=['Count'])
#     df.reset_index(inplace=True)
#     df.columns = ['Sentiment', 'Count']

#     fig, ax = plt.subplots()
#     sns.barplot(x='Sentiment', y='Count', data=df, ax=ax)
#     plt.title("Sentiment Distribution")
#     st.pyplot(fig)

#     st.write("Coverage Differences:")
#     for diff in data['Comparative Sentiment Score']['Coverage Differences']:
#         st.write(f"- {diff['Comparison']}")
#         st.write(f"  Impact: {diff['Impact']}")

#     st.write("Topic Overlap:")
#     topic_overlap = data['Comparative Sentiment Score']['Topic Overlap']
#     st.write(f"Common Topics: {', '.join(topic_overlap['Common Topics'])}")
#     for article, topics in topic_overlap.items():
#         if article != 'Common Topics':
#             st.write(f"{article}: {', '.join(topics)}")

#     st.subheader("Final Sentiment Analysis")
#     st.write(data['Final Sentiment Analysis'])

#     st.subheader("Audio Summary (Hindi)")
#     st.audio(data['Audio'], format='audio/wav')

# if __name__ == "__main__":
#     main()
import streamlit as st
import requests

# Function to fetch data from the FastAPI backend
def fetch_company_data(company_name):
    api_url = "http://127.0.0.1:8000/analyze_company"  # Adjust if deployed elsewhere
    response = requests.post(api_url, json={"name": company_name})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

# Main Streamlit app
def main():
    st.title("Company News Analyzer")
    company_name = st.text_input("Enter company name:")

    if st.button("Analyze"):
        with st.spinner("Analyzing news..."):
            try:
                data = fetch_company_data(company_name)
                display_results(data)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def display_results(data):
    st.subheader("News Analysis Results")
    for article in data["Articles"]:
        st.write(f"**Title:** {article['Title']}")
        st.write(f"**Summary:** {article['Summary']}")
        st.write(f"**Sentiment:** {article['Sentiment']}")
        st.write(f"**Topics:** {', '.join(article['Topics'])}")
        st.write("---")

    st.subheader("Comparative Analysis")
    sentiment_dist = data["Comparative Sentiment Score"]["Sentiment Distribution"]
    for sentiment, count in sentiment_dist.items():
        st.write(f"{sentiment}: {count}")

    topic_overlap = data["Comparative Sentiment Score"]["Topic Overlap"]
    st.write("**Common Topics:**", ", ".join(topic_overlap["Common Topics"]))
    for article, topics in topic_overlap["Unique Topics"].items():
        st.write(f"{article}: {', '.join(topics)}")

    st.subheader("Final Sentiment Analysis")
    st.write(data["Final Sentiment Analysis"])

    st.subheader("Audio Summary (Hindi)")
    audio_bytes = data["Audio"]
    st.audio(audio_bytes, format="audio/wav")

if __name__ == "__main__":
    main()
