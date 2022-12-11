import pymongo
import json

with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)

client = pymongo.MongoClient(sc_python['MONGODB'])
db = client['stockDB']

price_collection = db['stock_price']

# print(price_collection.delete_one({'ticker':'aapl'}))
print(price_collection.find_one({'ticker':'aapl'}))
