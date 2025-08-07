# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the CSV
# df = pd.read_csv('reviews_with_sentiment.csv')

# # Group by city and calculate average sentiment score
# sentiment_by_city = df.groupby('city')['sentiment_score'].mean().sort_values(ascending=False)

# # Plotting
# plt.figure(figsize=(12, 6))
# sentiment_by_city.plot(kind='bar', color='skyblue')
# plt.title('Average Sentiment Score by City')
# plt.xlabel('City')
# plt.ylabel('Average Sentiment Score')
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()
# plt.grid(axis='y')
# plt.show()







# import seaborn as sns

# sns.countplot(data=df, x='sentiment_label')
# plt.title("Sentiment Label Distribution")
# plt.xlabel("Sentiment")
# plt.ylabel("Number of Reviews")
# plt.show()



# keyword_rate = df.groupby('city')['keyword_match'].mean().sort_values(ascending=False) * 100
# keyword_rate.plot(kind='bar', figsize=(10, 5), title='Keyword Match % by City')
# plt.ylabel('Match %')
# plt.xticks(rotation=45)
# plt.show()





import pandas as pd
import numpy as np
import re

# Load the dataset
df = pd.read_csv("reviews_with_sentiment.csv")

# Step 1: Drop completely empty rows
df.dropna(how='all', inplace=True)

# Step 2: Drop duplicates
df.drop_duplicates(inplace=True)

# Step 3: Strip whitespace from string columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Step 4: Fill missing values if needed
df['review'].fillna("No review", inplace=True)
df['city'].fillna("Unknown", inplace=True)

# Step 5: Remove non-ASCII characters from text fields
df['review'] = df['review'].apply(lambda x: re.sub(r'[^\x00-\x7F]+', ' ', x))

# Step 6: Clean sentiment_score (remove outliers)
q1 = df['sentiment_score'].quantile(0.25)
q3 = df['sentiment_score'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

df = df[(df['sentiment_score'] >= lower_bound) & (df['sentiment_score'] <= upper_bound)]

# Step 7: Save cleaned file
df.to_csv("cleaned_reviews.csv", index=False)

print("✅ Cleaned data saved to cleaned_reviews.csv")
