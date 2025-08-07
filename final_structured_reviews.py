import pandas as pd
from textblob import TextBlob
import re

# ✅ Load data
df = pd.read_csv('reviews_with_sentiment.csv')

# ✅ Clean missing or invalid entries
df = df[df['review'].notnull() & (df['review'].str.strip() != '')]

# ✅ Define keyword list (expandable)
keywords = [
    'booth', 'booths', 'chair', 'chairs', 'table', 'tables', 'stool', 'stools',
    'bench', 'benches', 'seat', 'seating', 'furniture', 'uncomfortable', 'comfortable',
    'cramped', 'crowded', 'tight', 'clean', 'dirty', 'sticky', 'wobbly', 'layout',
    'space', 'spacing', 'hard to sit', 'hard to reach', 'height', 'legroom', 'cushion',
    'bar seating', 'high top', 'low table', 'counter', 'counters', 'railing', 'railings',
    'divider', 'queue', 'queue line', 'stanchion', 'wood', 'oak', 'timber', 'wood sign',
    'timber sign', 'wooden sign', 'signage', 'decor', 'paneling'
]

# ✅ Preprocess text
def clean_text(text):
    return re.sub(r'[^\w\s]', '', str(text).lower())

df['cleaned_review'] = df['review'].apply(clean_text)

# ✅ Flag relevant reviews
def match_keywords(text):
    return any(kw in text for kw in keywords)

df['keyword_match'] = df['cleaned_review'].apply(match_keywords)

# ✅ Sentiment analysis (optional, for extra insight)
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

df['sentiment_score'] = df['cleaned_review'].apply(get_sentiment)

# ✅ Label sentiment
def label_sentiment(score):
    if score > 0.2:
        return 'positive'
    elif score < -0.2:
        return 'negative'
    else:
        return 'neutral'

df['sentiment_label'] = df['sentiment_score'].apply(label_sentiment)

# ✅ Filter relevant reviews
relevant_reviews = df[df['keyword_match'] == True]

# ✅ Surface frequent complaint topics (bonus)
from collections import Counter

all_keywords_in_relevant = []
for review in relevant_reviews['cleaned_review']:
    found = [kw for kw in keywords if kw in review]
    all_keywords_in_relevant.extend(found)

top_keywords = Counter(all_keywords_in_relevant).most_common(15)

# ✅ Export to Excel with two sheets
with pd.ExcelWriter("final_structured_reviews.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="All Reviews", index=False)
    relevant_reviews.to_excel(writer, sheet_name="Relevant Reviews", index=False)

# ✅ Optional: print top pain points
print("\n🔥 Top Pain Point Keywords:")
for kw, count in top_keywords:
    print(f"{kw}: {count}")



with open("summary.txt", "w") as f:
    f.write("📍 Summary of Trends and Gaps\n")
    f.write("=============================\n\n")

    f.write("🪑 Common Pain Points (Top Keywords):\n")
    for kw, count in top_keywords:
        f.write(f"- {kw} ({count} mentions)\n")

    f.write("\n📍 Geographic Observations:\n")
    city_counts = relevant_reviews['city'].value_counts()
    for city, count in city_counts.items():
        f.write(f"- {city}: {count} relevant reviews\n")

    f.write("\n🧠 Sample Quotes:\n")
    for idx, row in relevant_reviews.head(3).iterrows():
        f.write(f"\n• \"{row['review']}\" – {row['city']}, {row['review_date']}\n")
