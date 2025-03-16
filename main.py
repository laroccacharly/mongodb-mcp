from pymongo import MongoClient

# Step 1: Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Step 2: Create or connect to a database
db = client['example_database']

# Step 3: Create or connect to a collection
collection = db['example_collection']

# Step 4: Insert a document
document = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 28
}
collection.insert_one(document)

# Step 5: Query the document
query = {"name": "John Doe"}
result = collection.find_one(query)
print(result)

# Step 6: Update a document
updated_document = {"$set": {"age": 29}}
collection.update_one(query, updated_document)


# Step 8: Close the connection
client.close()