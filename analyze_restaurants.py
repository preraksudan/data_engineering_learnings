import json
import pandas as pd

# Step 1: Load JSON data from file
with open('output.json', 'r') as file:
    data = json.load(file)

# Step 2: Normalize the JSON
records = []
for restaurant in data:
    base_info = {
        "address": restaurant.get("address"),
        "city": restaurant.get("city"),
        "country": restaurant.get("country"),
        "categories": ", ".join(restaurant.get("categories", []))  # Combine into single string
    }
    
    # Multiple descriptions → create separate rows
    for desc in restaurant.get("descriptions", []):
        record = base_info.copy()
        record["review_date"] = desc.get("dateSeen")
        record["review"] = desc.get("value")
        record["source_url"] = desc.get("sourceURLs", [None])[0]  # Get first URL if exists
        records.append(record)

# Step 3: Create DataFrame
df = pd.DataFrame(records)

# Optional: Save to Excel/CSV if needed
df.to_csv('restaurant_reviews.csv', index=False)
# df.to_excel('restaurant_reviews.xlsx', index=False)

# Step 4: Basic Analytics
print("🔍 Sample data:")
print(df.head())

# Example: Top 5 cities with most reviews
print("\n🏙️ Top 5 cities with most reviews:")
print(df['city'].value_counts().head())

# Example: Word frequency from all reviews
from collections import Counter
import re

all_reviews = " ".join(df['review'].dropna()).lower()
words = re.findall(r'\b\w+\b', all_reviews)
common_words = Counter(words).most_common(10)

print("\n📝 Most common words in reviews:")
for word, freq in common_words:
    print(f"{word}: {freq}")
