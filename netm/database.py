from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import json
from mongoengine import *
import logging

connect('netm')
logger = logging.getLogger(__name__)

class Customer(Document):
    name = StringField(required=True)
    address = StringField()

class Database():

    col_name = "customers"

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client["netm"]
        self.col = self.db[self.col_name]

    def customers(self):
        self.col = self.db['customers']
        return self.col


db = Database()

if __name__ == "__main__":
    print("Netm is working")