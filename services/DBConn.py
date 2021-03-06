from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#Username = bartermaster, password=barterpassword, databasename = hunter_barter
client = MongoClient("mongodb://bartermasteruser:barterpassword@cluster0-shard-00-00-dmzwb.mongodb.net:27017,cluster0-shard-00-01-dmzwb.mongodb.net:27017,cluster0-shard-00-02-dmzwb.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
adminDB = client.admin
db = client.hunter_barter
# Issue the serverStatus command and print the results
serverStatusResult=adminDB.command("serverStatus")
pprint(serverStatusResult)