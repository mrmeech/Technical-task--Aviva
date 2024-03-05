#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import necessary python libraries
import pandas as pd
import json
from collections import Counter
import uuid

# Load the JSON data
with open('input_data.json', 'r') as file:
    data = json.load(file)

# Create a list to store word counts for each petition
word_counts_list = []

# Extract and count words for each petition
for petition in data:
    text = petition['abstract']['_value'].lower() + ' ' + petition['label']['_value'].lower()
    
    # Count words of 5 or more letters
    word_counts = Counter(word for word in text.split() if len(word) >= 5)
    
    # Generate a random UUID as petition_id
    word_counts['petition_id'] = str(uuid.uuid4())
    
    # Append the petition_id and word counts to the list
    word_counts_list.append(word_counts)

# Create a DataFrame from the list
df = pd.DataFrame(word_counts_list)

# Select the 20 most common words (excluding 'petition_id')
common_words = df.drop(columns= ['petition_id']).sum().nlargest(20).index

# Create a new DataFrame with only the selected columns
df_final = df[['petition_id'] + list(common_words)]

# Fill NaN values with 0
df_final = df_final.fillna(0)

# Save the DataFrame to a CSV file
df_final.to_csv('clean_df.csv', index=False)

