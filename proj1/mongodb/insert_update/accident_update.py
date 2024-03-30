import argparse
from pymongo import MongoClient

# Function to update a accident document
def update_accident(db, identifier):
    # Find the accident document by its _id
    accident = db.accidents.find_one({"_id": identifier})

    if accident is None:
        print("Accident not found.")
        return

    # Prompt the user to update each field except for "_id"
    for key in accident.keys():
        if key != "_id" or key != "_id" != "MC":
            new_value = input(f"Enter new value for {key} (or press Enter to keep current value): ").strip()
            if new_value:
                accident[key] = new_value

    # Update the accident document in the database
    db.accidents.update_one({"_id": identifier}, {"$set": accident})
    print("Accident updated successfully.")
    print("Accident saved with the original ID: ", identifier)


###############################################################################################
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Update a accident in the database")
parser.add_argument("--id", type=str, required=True, help="Identifier of the accident to update")
args = parser.parse_args()

# Connect to the MongoDB server
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.test  # Replace with your actual database name

# Call the update function with the provided identifier
update_accident(db, args.id)
