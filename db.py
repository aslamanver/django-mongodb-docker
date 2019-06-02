import pymongo

myclient = pymongo.MongoClient("mongodb://0.0.0.0:27017/")

mydb = myclient["mydatabase"]

print(myclient.list_database_names())