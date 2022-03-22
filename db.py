from pymongo import MongoClient

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import re
import json
mongo_client = MongoClient('mongo', 27017)
db_version = 1
account_db = mongo_client["account_db"+str(db_version)]
users_id_collection = account_db["id_counter"]
account_info = account_db["account_info"]
id_query = {"field": "key"}

#registration content
def db_get_content(some_data_collection):
    cur = some_data_collection.find()
    not_first = 0
    ret = "["
    for i in cur:
        if not_first == 1:
            ret += ","
        not_first = 1
        ret += "{"
        ret += "\"id\":" + str(i["id"])

        ret += ",\"firstname\":\"" + i["firstname"]
        ret += "\""

        ret += ",\"lastname\":\"" + i["lastname"]
        ret += "\""

        ret += ",\"username\":\""+ i["username"]
        ret += "\""

        ret += ",\"password\":\"" + i["password"]
        ret += "\""
        ret += "}"
    ret += "]"
    ret_len = len(ret)

    if ret_len == 1:
        ret="[{}]"
    return ret

def next_id():

    size = users_id_collection.count_documents(id_query)
    if size == 0:
        firstId = 1
        users_id_collection.insert_one({'id': firstId,'field':'key'})
        return firstId
    else:
        current_id = users_id_collection.find(id_query)[0]['id']
        nextId = current_id + 1
        newvalues = {"$set": {"id": nextId}}
        users_id_collection.update_one(id_query,newvalues)
        return nextId
def user_exist(username):

    query = {"username": username}
    data = list(account_info.find(query, {"_id": False, "id": True, "username": True}))
    return len(data) > 0


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
def password_hash_gen(password):
    try:
        hash = generate_password_hash(password, "sha256")
    except:
        print("error with hash")

    if check_password_hash(hash,password) and hash != password:
        return hash
    else:
        return 0
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





def login_validation(username, password):

    query = {"username": username}
    data = list(account_info.find(query, {"_id": False, "id": True, "username": True, "password": True}))

    if len(data) != 1:
        return False


    jsonString = re.sub("\'", "\"", str(data[0]))
    dataDict = json.loads(jsonString)

    if check_password_hash(dataDict["password"], password):
        return True
    else:
        return False

def user_data(username):

    query = {"username": username}
    data = list(account_info.find(query,{"_id": False,"password":False}))


    if len(data) != 1:
        return False
    jsonString = re.sub("\'", "\"", str(data[0]))
    #flush("json: "+str(jsonString))

    userdata = json.loads(jsonString)

    return userdata #return userdata as dictionary

