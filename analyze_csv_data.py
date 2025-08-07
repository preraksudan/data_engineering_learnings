import pandas as pd

import nltk
nltk.download('punkt')


from textblob import TextBlob


# Load your file
df = pd.read_csv('restaurant_reviews.csv')

# Check the first few rows
print(df.head())



import re

def clean_review(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['cleaned_review'] = df['review'].apply(clean_review)



# Define keywords
keywords = ['bacon', 'cheeseburger', 'service', 'staff', 'price', 'atmosphere']

# Flag reviews that mention any of the keywords
df['keyword_match'] = df['cleaned_review'].apply(
    lambda x: any(word in x for word in keywords)
)




from textblob import TextBlob

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

df['sentiment_score'] = df['cleaned_review'].apply(get_sentiment)

# Classify sentiment
df['sentiment_label'] = df['sentiment_score'].apply(
    lambda score: 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'
)




# Filter only relevant reviews
relevant_reviews = df[df['keyword_match'] == True]

# Show counts
print("Total reviews:", len(df))
print("Relevant reviews:", len(relevant_reviews))

# Sentiment distribution
print(df['sentiment_label'].value_counts())



df.to_csv('processed_reviews.csv', index=False)


text = "The food was great and the staff were friendly."
blob = TextBlob(text)

# Sentiment analysis
print(blob.sentiment)
# Output: Sentiment(polarity=0.85, subjectivity=0.75)