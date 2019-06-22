from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import json
from mongoengine import *
import logging

connect('netm', host='mongodb.netm', port=27017)
logger = logging.getLogger(__name__)


class Customer(Document):
    email = StringField()
    password = StringField()


class Members(Document):
    email = StringField()
    password = StringField()
    first_name = StringField()
    last_name = StringField()
    gender = StringField()
    dob = StringField()
    user_type = StringField()
    mobile = StringField()
    status = IntField()
    verification_code = StringField()


# Don't refer after this line
class Database():

    col_name = "members"

    def __init__(self):
        self.client = MongoClient('mongodb://mongodb.netm:27017')
        self.db = self.client["netm"]
        self.col = self.db[self.col_name]

    def members(self):
        self.col = self.db['members']
        return self.col

    def users(self):
        self.col = self.db['users']
        return self.col
        
db = Database()

if __name__ == "__main__":
    print("Netm is working")
