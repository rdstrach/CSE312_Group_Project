from flask_server import db
from pymongo import MongoClient
import sys
import string

def escape_html(message: string)->string:
    # Set escape substitutes
    escape_amp = "&amp"
    escape_lt = "&lt"
    escape_gt = "&gt"

    # Replace characters
    message = message.replace("&", escape_amp)
    message = message.replace("<", escape_lt)
    message = message.replace(">", escape_gt)

    return message

# Loads message into database: "text messages" collection
def loads_tm(username: string, text_message: string):
    server = db()
    tm_collection = server["text messages"]

    id = 0  # Initialize id to 0 for first id to be 1
    # Iterate through database and create new id
    for line in tm_collection.find():
        if line.get("id") != None:
            id = int(line.get("id"))
    id += 1
  
    # Parse request body containing JSON and create dictionary to be inserted
    dict = { "id" : str(id),  "username" : username, "message" : escape_html(text_message) }

    # Insert dictionary in database
    tm_collection.insert_one(dict)
    

def print_tm():
    server = db()
    tm_collection = server["text messages"]
    for line in tm_collection.find():
        print(line)
