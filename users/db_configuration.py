import pymongo

url_connection = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url_connection)

db = client['users']