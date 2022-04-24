from pymongo import MongoClient


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