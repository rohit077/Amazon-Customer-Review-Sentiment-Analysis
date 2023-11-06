import streamlit as st
import json
import openai
import pandas as pd

# Set your OpenAI API key here
os.environ['OPENAI_API_KEY'] = "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"

st.title("Amazon Review Sentiment Analysis")
#st.config(layout=wide)

# Upload the JSON file with Amazon reviews
uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

if uploaded_file is not None:
    # Read and parse the JSON file
    data = json.load(uploaded_file)

    # Display the loaded data
    st.write("Loaded Reviews:")
    st.write(data)

    # Perform sentiment analysis on the reviews
    st.write("Sentiment Analysis Results:")

    # for reviews in data:
    #     for review in reviews:
    #         if "body" in review:
    #             review_text = review["body"]
    #             st.write(f"Review Text: {review_text}")

    #             prompt = f"""
    #             You're an Amazon Sentiment Analyst with 10+ years of experience. You have a deep understanding of product reviews and can accurately determine sentiment. You've been provided with the following review:
    #             '{review_text}'
    #             Please rate how positive or negative this review is on a scale from 0 to 10, where 0 is extremely negative and 10 is extremely positive.
    #             """
                
    #             response = openai.Completion.create(
    #                 engine="text-davinci-003",
    #                 prompt=prompt,
    #                 max_tokens=1,
    #             )
    #             sentiment = response.choices[0].text.strip()
    #             st.write(f"Sentiment: {sentiment}")
    #         else:
    #             st.write("Review does not contain 'body' text.")



# Create a list to store sentiment data
    sentiment_data = []

    for reviews in data:
        for review in reviews:
            if "body" in review:
                review_text = review["body"]

                if not review_text:
                    sentiment_data.append(None)
                else:
                    prompt = f"""
                    You're an Amazon Sentiment Analyst with 10+ years of experience. You have a deep understanding of product reviews and can accurately determine sentiment. You've been provided with the following review:
                    '{review_text}'
                    Please rate how positive or negative this review is on a scale from 0 to 10, where 0 is extremely negative and 10 is extremely positive.
                    """

                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=1,
                    )
                    sentiment_text = response.choices[0].text.strip()

                    if sentiment_text:
                        sentiment = float(sentiment_text)
                        sentiment_data.append(sentiment)
                    else:
                        sentiment_data.append(None)
            else:
                sentiment_data.append(None)

    # Create a DataFrame from the sentiment data
    df = pd.DataFrame(sentiment_data, columns=["Sentiment"])

    # Perform sentiment classification (you can customize the threshold)
    df["Sentiment_Label"] = df["Sentiment"].apply(lambda x: "Positive" if x is not None and x >= 5 else "Negative" if x is not None and x <= 5 else "Neutral")

    # Calculate the percentage of positive, negative, and neutral sentiment
    sentiment_counts = df["Sentiment_Label"].value_counts()

    # Ensure that the labels exist before calculations
    positive_percentage = (sentiment_counts.get("Positive", 0) / df.shape[0]) * 100
    negative_percentage = (sentiment_counts.get("Negative", 0) / df.shape[0]) * 100
    neutral_percentage = (sentiment_counts.get("Neutral", 0) / df.shape[0]) * 100

    # Display the percentages
    st.write(f"Total Reviews: df.shape[0]")
    st.write(f"Positive Reviews: {positive_percentage:.2f}%")
    st.write(f"Negative Reviews: {negative_percentage:.2f}%")
    st.write(f"Neutral Reviews: {neutral_percentage:.2f}%")
