from pymongo import MongoClient

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import re
import json
mongo_client = MongoClient('mongo', 27017)
version = 1
"""
account_db: contains 2 collections, user account info,
users_id_collection: collection for id increment. Only used by next_id
"""
account_db = mongo_client["account_db"+str(version)]
users_id_collection = account_db["id_counter"]
account_info = account_db["account_info"]
id_query = {"field": "key"}

"""
create_user(first_name,last_name,username,password,password_again)
returns empty set if userdata valid and created
returns set of strings, with user error description 
"""
def create_user(first_name,last_name,username,password,password_again):
    data = dict()
    val_ret=set()
    username= str(username).lower()
    val_ret = validate_registration_input(first_name, last_name, username, password, password_again)
    if (len(val_ret)!=0):
        return val_ret

    data["firstname"] = first_name
    data["lastname"] = last_name
    data["username"] = username
    password_hash=password_hash_gen(password)
    if password_hash == 0:
        val_ret.add("Potential error has occurred. Try another password or try again later.")
        return val_ret

    data["password"] = password_hash
    if len(val_ret) == 0:
        data["id"] = next_id()
        account_info.insert_one(data)
        return val_ret
    else:
        return val_ret

"""
def validate_registration_input(first_name, last_name, username, password, password_again)
returns empty set if user data is valid
returns set of strings, with user error description 

No changes to database done here
"""

def validate_registration_input(first_name, last_name, username, password, password_again):
    ret=set()
    username = str(username).lower()
    if not str(first_name).isalpha():
        ret.add("First name can only contain alphabetic characters")
    if not str(last_name).isalpha():
        ret.add("Last name can only contain alphabetic characters")
    if len(first_name) == 0:
        ret.add("No user input for first name.")
    if len(last_name) == 0:
        ret.add("No user input for last name.")
    if user_exist(username):
        ret.add("Username already exist.")
    if len(username) == 0:
        ret.add("No user input for username.")
    if len(password) == 0:
        ret.add("No user input for Password.")
    if len(password) < 8:
        ret.add("Password must be at least 8 characters long.")
    if password != password_again:
        ret.add("Passwords do not match")
    return ret

"""
def next_id()
Is is uses users_id_collection to count id's; will increment and return id
Called only for user_create()
req1-note: undefined behaviour if this value is nonpositive

req2-note: undefined behaviour if this value is nonpositive

"""
def next_id():

    size = users_id_collection.count_documents(id_query)
    if size == 0:
        firstId = 1  # should  be a positive start value req1-note
        users_id_collection.insert_one({'id': firstId,'field':'key'})
        return firstId
    else:
        current_id = users_id_collection.find(id_query)[0]['id']
        id_distance = 1 # this value must be a positive value req2-note
        nextId = current_id + id_distance
        newvalues = {"$set": {"id": nextId}}
        users_id_collection.update_one(id_query,newvalues)
        return nextId





"""
 login_validation(username, password)
 returns distinct positive ..integer type.. value "user id" if given correct username and password
 or returns -1 if otherwise
"""


def login_validation(username, password):
    username=str(username).lower()
    query = {"username": username}
    data = list(account_info.find(query, {"_id": False, "id": True, "username": True, "password": True}))

    if len(data) != 1:
        return -1


    jsonString = re.sub("\'", "\"", str(data[0]))
    dataDict = json.loads(jsonString)

    if check_password_hash(dataDict["password"], password):
        return dataDict["id"]
    else:
        return -1

"""
 def user_data(id)
    returns dictionary of all user data except password give the user id as integer
    returns bool FALSE if id doesn't exist, nonpositive values will return false,
     as long as next_id() begins at the value 1
"""
def user_data(id):

    query = {"id": id}
    data = list(account_info.find(query,{"_id": False,"password":False}))


    if len(data) != 1:
        return False
    jsonString = re.sub("\'", "\"", str(data[0]))

    userdata = json.loads(jsonString)

    return userdata #return userdata as dictionary

"""
def user_exist(username):
returns true if username already exist; username is not considered to be case sensitive;
used in validate_registration_input function to ensure there are no duplicate usernames

"""


def user_exist(username):
    username=str(username).lower()
    query = {"username": username}
    data = list(account_info.find(query, {"_id": False, "id": True, "username": True}))
    return len(data) > 0


"""
def password_hash_gen(password)
return password hash or 0 if hash parameter is typed in incorrectly 

"""


def password_hash_gen(password):
    try:
        hash = generate_password_hash(password, "sha256")
    except:
        print("error with hash")

    if check_password_hash(hash,password) and hash != password:
        return hash
    else:
        return 0