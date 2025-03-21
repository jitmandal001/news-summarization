
import streamlit as st
import requests
from fastapi import FastAPI
from api import router

app = FastAPI()

# Include the router from api.py
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Company Analysis API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)

# Function to fetch data from the FastAPI backend
def fetch_company_data(company_name):
    api_url = "http://Jman666/News-Article-Extraction.hf.space/analyze_company"  # Adjust if deployed elsewhere
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
