import dns
import pymongo

client = pymongo.MongoClient("mongodb+srv://Mark_2386300:2386300@cluster0.rpq32.mongodb.net/testdb?retryWrites=true&w=majority")
db = client['testdb']

collection = db['testcollection']

to_be_inserted = {'name':'Mark', 'comment':'Need to make sure this still works'}
id = collection.insert_one(to_be_inserted)

print(id.inserted_id)