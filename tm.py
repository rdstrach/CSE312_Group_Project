from flask_server import db
from pymongo import MongoClient
import sys
import string
from datetime import datetime
from pytz import timezone
import json

collection_name = "text messages"

# Loads message into database: "text messages" collection
def loads_tm(username: string, text_message: string):
    server = db()
    tm_collection = server[collection_name]

    id = 0  # Initialize id to 0 for first id to be 1
    # Iterate through database and create new id
    for line in tm_collection.find({}, {"_id": False}):
        if line.get("id") != None:
            id = int(line.get("id"))
    id += 1
    
    # Get and format current time
    time = datetime.now(timezone('America/New_York'))
    time = time.strftime("%m/%d/%Y %H:%M")

    # Parse request body containing JSON and create dictionary to be inserted
    dict = { "id" : str(id),  "username" : username, "message" : text_message, "time" : time, "votes" : str(0) }

    # Insert dictionary in database
    tm_collection.insert_one(dict)
    
# Returns all messages in database: "text messages" collection as an array
def returns_tm():
    server = db()
    tm_collection = server[collection_name]
    ret_list = []
    for line in tm_collection.find({}, {"_id": False}):
        ret_list.append(line)
    return ret_list

# Prints all in database: "text messages" collection
def prints_tm():
    server = db()
    tm_collection = server[collection_name]
    for line in tm_collection.find({}, {"_id": False}):
        print(line)
        sys.stdout.flush()
        sys.stderr.flush()

def upvotes_tm(json_string: string):
    server = db()
    tm_collection = server[collection_name]

    # Convert json string to dict
    message = json.loads(json_string)
    tm_id = message["id"]

    votes = 0
    # Iterate through database and find message to increment votes
    for line in tm_collection.find({}, {"_id": False}):
        if line.get("id") == tm_id:
            votes = int(line["votes"])
            votes += 1
            # line["votes"] = str(votes) # Can't directly manipulate db
            break
    
    # Update query
    search_query = { "id": tm_id }
    new_votes = { "$set": { "votes": str(votes) } }
    tm_collection.update_one(search_query, new_votes)