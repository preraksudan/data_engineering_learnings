import nltk
nltk.download('punkt')


import pandas as pd
from textblob import TextBlob



# Step 1: Load your CSV file
df = pd.read_csv("processed_reviews.csv")  # Replace with your actual CSV file name

# Step 2: Define a function to analyze sentiment
def get_sentiment(text):
    blob = TextBlob(str(text))  # Convert to string in case of NaN
    return blob.sentiment.polarity

# Step 3: Apply sentiment function to 'review' column
df['sentiment'] = df['review'].apply(get_sentiment)

# Step 4: Categorize sentiment
def label_sentiment(polarity):
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

df['sentiment_label'] = df['sentiment'].apply(label_sentiment)

# Step 5: Save to a new CSV
df.to_csv("reviews_with_sentiment.csv", index=False)

print("Sentiment analysis complete! Results saved to 'reviews_with_sentiment.csv'")
