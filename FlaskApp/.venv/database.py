import requests
import time
from pymongo import MongoClient
import schedule

#Connecting to MongoDB
client = MongoClient("mongodb+srv://FinalProject_GP6:group_6@cluster0.4e58jly.mongodb.net/?retryWrites=true&w=majority")
database = client["crypto"]
collection = database["data"]

#Method to Insert all the data to database
def insertIntoMongoDb():
    req = requests.get("https://api.wazirx.com/sapi/v1/tickers/24hr")
    if req.status_code == 200:
        data = req.json()
        collection.insert_many(data)

insertIntoMongoDb()

#Pseudo batch that runs every 24 hours to acquire data and store in the database
schedule.every(23).hours.do(insertIntoMongoDb)
while 1:
    schedule.run_pending()
    time.sleep(1)