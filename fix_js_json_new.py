import json
import pandas as pd

# Load JSON data
with open('output.json', 'r') as f:
    data = json.load(f)

# Normalize the JSON structure (flatten nested fields)
df = pd.json_normalize(data, record_path='reviews', meta=['url'])

# Define keyword filters
keywords = ['furniture', 'seating', 'layout', 'signage', 'table', 'counter', 'space', 'chairs']

# Create a new column to flag if the description is relevant
df['relevant'] = df['value'].str.lower().apply(
    lambda text: any(kw in text for kw in keywords) if isinstance(text, str) else False
)

# Filtered DataFrame
df_relevant = df[df['relevant'] == True]

# Write both full and relevant data to Excel
with pd.ExcelWriter('parsed_reviews.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='All reviews', index=False)
    df_relevant.to_excel(writer, sheet_name='Relevant reviews', index=False)
