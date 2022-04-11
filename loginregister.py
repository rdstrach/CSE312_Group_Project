from db import *
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
"""

create_user(first_name,last_name,username,password,password_again)
Add user data to database
if successful 
user account has been created;
returns empty set; 
else
no data modified/added to database
returns set of string(s), with user error descriptions, 
"""


def create_user(first_name, last_name, username, password, password_again):
    data = dict()
    val_ret = set()
    username = str(username).lower()
    val_ret = validate_registration_input(first_name, last_name, username, password, password_again)
    if len(val_ret) != 0:
        return val_ret

    data["firstname"] = first_name
    data["lastname"] = last_name
    data["username"] = username
    password_hash = password_hash_gen(password)
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
returns set of strings, with user error descriptions

No changes made to database in this function
"""


def validate_registration_input(first_name, last_name, username, password, password_again):
    ret = set()
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
 login_validation(username, password)
 returns distinct positive ..integer type.. value "user id" if given correct username and password
 or returns -1 if otherwise
"""


def login_validation(username, password):
    username = str(username).lower()
    query = {"username": username}
    data = list(account_info.find(query, {"_id": False, "id": True, "username": True, "password": True}))

    if len(data) != 1:
        return -1

    json_string = re.sub("\'", "\"", str(data[0]))
    data_dict = json.loads(json_string)

    if check_password_hash(data_dict["password"], password):
        return data_dict["id"]
    else:
        return -1


"""
 def user_data(id)
    returns dictionary of all user data except password give the user id as integer
    returns bool FALSE if id doesn't exist, nonpositive values will return false

"""


def user_data(id):
    if id <= 0:
        return False
    query = {"id": id}
    data = list(account_info.find(query, {"_id": False, "password": False}))

    if len(data) != 1:
        return False
    json_string = re.sub("\'", "\"", str(data[0]))

    userdata = json.loads(json_string)

    return userdata  # return userdata as dictionary


"""
def user_exist(username):
returns true if username already exist; username is not considered to be case sensitive;
used in validate_registration_input function to ensure there are no duplicate usernames
query user
"""


def user_exist(username):
    username = str(username).lower()
    query = {"username": username}
    data = list(account_info.find(query, {"_id": False, "id": True, "username": True}))
    return len(data) > 0


"""
def password_hash_gen(password)
return password hash or 0 if hash parameter is typed in incorrectly 

"""


def password_hash_gen(password):
    try:
        hash_password = generate_password_hash(password, "sha256")
    except:
        print("Error with hash")
        return 0

    if check_password_hash(hash_password, password) and hash_password != password:
        return hash_password

    return 0


"""
def next_id()
uses collection users_id_collection to count id's; will increment and return id
Called only for user_create()

req1-note: undefined behaviour if this value is non-positive
req2-note: undefined behaviour if this value is non-positive

"""


def next_id():
    size = users_id_collection.count_documents(id_query)
    if size == 0:
        firstId = 1  # should  be a positive start value... req1-note
        users_id_collection.insert_one({'id': firstId, 'field': 'key'})
        return firstId
    else:
        current_id = users_id_collection.find(id_query)[0]['id']
        id_distance = 1  # this value must be a positive value... req2-note
        nextId = current_id + id_distance
        newvalues = {"$set": {"id": nextId}}
        users_id_collection.update_one(id_query, newvalues)
        return nextId

#----------- login in list
'''
def is_signed(user_id):
Uses logged_in collection to check if user is logged in
Returns True if user is logged in
Returns False if user is not logged in

'''

def is_signed(user_id):

    user_id = int(user_id)
    query = {"id": user_id}
    data = list(logged_in.find(query, {"_id": False, "id": True}))
    return len(data) > 0
'''
def login_user(user_id):
Insert id logged_in collection
Returns True if user exist and was not logged
Returns False if user does not exist or is already logged in

'''
def login_user(user_id):

    user = dict()
    if not str(user_id).isdigit():
        return False
    input = int(user_id)

    user_info = user_data(input)

    login_data= dict()
    if user_info==False:
        return False
    if input!=user_info['id']:
        return False
    if is_signed(input):
        return False #already signed in
    user.update({"id": user_info['id']})

    logged_in.insert_one(user)
    return True
'''
def login_list():
Returns: list of logged in users
Returns: empty list if no users are logged on
'''
def login_list():
    cur = logged_in.find()
    ret= list()
    for i in cur:
        ret.append(user_data(i['id'])['username'])
    return ret