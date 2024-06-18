import requests
import hashlib
import time
import pandas as pd
import sqlite3
import json

# Get countries data
response = requests.get("https://restcountries.com/v3.1/all")
countries = response.json()

data = []

for country in countries:
    start_time = time.perf_counter()
    
    # Get country name
    name = country.get('name', {}).get('common', 'Unknown')
    
    # Get country region
    region = country.get('region', 'Unknown')
    
    # Get country languages
    languages = country.get('languages', {})
    language_names = ', '.join(languages.values())
    
    # Encrypt language using SHA1
    language_hash = hashlib.sha1(language_names.encode('utf-8')).hexdigest().upper()
    
    end_time = time.perf_counter()

    # Time in milliseconds
    total_time = (end_time - start_time) * 1000

    data.append({
        'Region': region,
        'City Name': name,
        'Language': language_hash,
        'Time_ms': total_time
    })

# Pandas DataFrame
df = pd.DataFrame(data)

# Calculation of times
total_time = df['Time_ms'].sum()
average_time = df['Time_ms'].mean()
min_time = df['Time_ms'].min()
max_time = df['Time_ms'].max()

# Show times in console
print(f"Total Time: {total_time:.2f} ms")
print(f"Average Time: {average_time:.2f} ms")
print(f"Min Time: {min_time:.2f} ms")
print(f"Max Time: {max_time:.2f} ms")

df['Time'] = df['Time_ms'].apply(lambda x: f"{x:.2f} ms")

df.drop(columns=['Time_ms'], inplace=True)

# Save DataFrame in SQLite Database
with sqlite3.connect('data.db') as conn:
    df.to_sql('data', conn, if_exists='replace', index=False)

# Save DataFrame as JSON file
df.to_json('data.json', orient='records', lines=True)