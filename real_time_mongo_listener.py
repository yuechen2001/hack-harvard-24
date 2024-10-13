# real_time_mongo_listener.py
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from hedera_utils import store_transaction_on_blockchain

# Load environment variables
load_dotenv()

# Set up MongoDB client
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MongoDB URI not set. Please check your .env file.")

# Connect to MongoDB using the correct connection string
client = MongoClient("mongodb+srv://vitthal:vitthal123@cluster0.fzcfu.mongodb.net/")
db = client["hackharvard"]  # Use the correct database name 'hackharvard'
consumer_collection = db["household_rec"]  # The collection where you store the records


def watch_consumer_rec_collection():
    try:
        # Watch for new inserts in the consumer_rec collection
        with consumer_collection.watch(
            [{"$match": {"operationType": "insert"}}]
        ) as stream:
            for change in stream:
                # Get the inserted document
                new_transaction = change["fullDocument"]
                print(f"New transaction detected: {new_transaction}")

                # Store the new transaction on Hedera Blockchain
                txn_id = store_transaction_on_blockchain(new_transaction)
                if txn_id:
                    print(
                        f"Stored transaction {new_transaction['_id']} on blockchain with txn ID {txn_id}"
                    )
                else:
                    print(
                        f"Failed to store transaction {new_transaction['_id']} on blockchain"
                    )
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {str(e)}")


# Call the function to start watching the collection in real-time
watch_consumer_rec_collection()
