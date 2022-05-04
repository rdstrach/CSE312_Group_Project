from db import db, get_user_info
import sys
import string
from datetime import datetime
from pytz import timezone

collection_name = "text messages"

# Loads message into database: "text messages" collection
def loads_tm(username: string, text_message: string):
    server = db()
    tm_collection = server[collection_name]

    id = 0  # Initialize id to 0 for first id to be 1
    # Iterate through database and create new id
    for line in tm_collection.find():
        if line.get("id") != None:
            id = int(line.get("id"))
    id += 1
    
    # Get and format current time
    time = datetime.now(timezone('America/New_York'))
    time = time.strftime("%m/%d/%Y %H:%M")

    # Parse request body containing JSON and create dictionary to be inserted
    dict = { "id" : str(id),  "username" : username, "message" : text_message, "time" : time }

    # Insert dictionary in database
    tm_collection.insert_one(dict)
    
# Returns all messages in database: "text messages" collection as an array
def returns_tm():
    server = db()
    tm_collection = server[collection_name]
    ret_list = []
    for line in tm_collection.find():
        user_info = get_user_info(line['username'])
        line['image'] = user_info['image']
        line['firstname'] = user_info['firstname']
        line['lastname'] = user_info['lastname']
        ret_list.append(line)
    return ret_list

# Prints all in database: "text messages" collection
def prints_tm():
    server = db()
    tm_collection = server[collection_name]
    for line in tm_collection.find():
        print(line)
        sys.stdout.flush()