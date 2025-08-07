import pandas as pd
from textblob import TextBlob

# Step 1: Load CSV
df = pd.read_csv("reviews_with_sentiment.csv")

# Step 2: Basic cleaning (drop nulls and reset index)
df.dropna(subset=['review'], inplace=True)
df.reset_index(drop=True, inplace=True)

# Step 3: Sentiment Analysis using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

df['sentiment_score'] = df['review'].apply(get_sentiment)

# Step 4: Sentiment Category
def classify_sentiment(score):
    if score > 0.2:
        return 'positive'
    elif score < -0.2:
        return 'negative'
    else:
        return 'neutral'

df['sentiment_label'] = df['sentiment_score'].apply(classify_sentiment)

# Step 5: Insights
print("🔹 Sentiment Counts:")
print(df['sentiment_label'].value_counts())

print("\n🔹 Average Sentiment Score:")
print(df['sentiment_score'].mean())

print("\n🔹 Top 5 Most Positive Reviews:")
print(df.sort_values(by='sentiment_score', ascending=False)[['review', 'sentiment_score']].head())

print("\n🔹 Top 5 Most Negative Reviews:")
print(df.sort_values(by='sentiment_score')[['review', 'sentiment_score']].head())

# Step 6: Export Final Data
df.to_csv("final_review_analysis.csv", index=False)
print("\n✅ Exported to final_review_analysis.csv")
