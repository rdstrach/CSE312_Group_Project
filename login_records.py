'''
Filename: login_records
File Created by Ryan Strachan
Contains functions for accessing and modifing "logined_in" collection
File edited by:  ...
'''

from db import *
from loginregister import user_data


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