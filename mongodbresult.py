from pymongo import MongoClient

# Connect to the MongoDB instance
client = MongoClient('mongodb://localhost:27017/')

# Access the database and collection
db = client['HoundHunt']
collection = db['webscraped']

# Create a text index on the 'html' field
collection.create_index([('html', 'text')])

# Define the search term
search_term = 'gentleman'

# Search for the search term and rank the results
results = collection.find(
    {'$text': {'$search': search_term}},
    {'score': {'$meta': 'textScore'}, 'url': 1}
).sort([('score', {'$meta': 'textScore'})])

# Print the results
for result in results:
    print(result['url'], result['score'])
