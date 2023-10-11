from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["test"]
collection = db["locations"]

# Specify the path to your JSON file
json_file = "NEW_locations.json"

# Read and parse the JSON file
with open(json_file, "r") as file:
    json_data = json.load(file)

# Iterate through your JSON data
for json_doc in json_data:
    # Check if a document with the same _id exists
    existing_doc = collection.find_one({"_id": json_doc["_id"]})

    if existing_doc:
        # Append values to the existing array
        collection.update_one(
            {"_id": json_doc["_id"]},
            {"$addToSet": {"accident_ids": {"$each": json_doc["accident_ids"]}}}
        )
    else:
        # Insert a new document
        collection.insert_one(json_doc)

# Close the MongoDB connection
client.close()
