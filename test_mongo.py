from pymongo import MongoClient

uri = "mongodb+srv://<username>:<password>@cluster.mongodb.net/"
client = MongoClient(uri)

try:
    print("✅ Connected successfully!")
    print("Available Databases:", client.list_database_names())
except Exception as e:
    print("❌ Connection failed:", e)
