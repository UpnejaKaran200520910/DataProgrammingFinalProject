from flask import Flask, jsonify, request
from flask import render_template
import requests
import time
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId


app = Flask(__name__)

#Connecting to MongoDB
client = MongoClient("mongodb+srv://FinalProject_GP6:group_6@cluster0.4e58jly.mongodb.net/?retryWrites=true&w=majority")
database = client["crypto"]
collection = database["data"]

#Method to find 5 highest element from the list
def FindTop5(list1, list2):
    dict = {}
    for i in range(5):
        top = max(list1)
        index = list1.index(top)
        symbol = list2[index]
        dict[symbol] = top
        list1.pop(index)
        list2.pop(index)
    return dict

def Volume():
    x = collection.find()
    ListofVolume = []
    ListofSymbol = []
    dict = {'Symbol':'Volume'}

    for item in x:
        volume = float(item.get('volume'))
        ListofVolume.append(volume)
        symbol = item.get('symbol')
        ListofSymbol.append(symbol)

    dict.update(FindTop5(ListofVolume,ListofSymbol))
    return dict

def profit():
    x = collection.find()
    ListofSymbol = []
    ListOfopenPrice = []
    ListofLastPrice = []
    Percent = []

    dict = {}

    for item in x:
        ListOfopenPrice.append(float(item.get('openPrice')))
        ListofLastPrice.append(float(item.get('lastPrice')))
        ListofSymbol.append(item.get('symbol'))

    for i in range(len(ListOfopenPrice)):
        percentage = ((ListofLastPrice[i]-ListOfopenPrice[i])/ListOfopenPrice[i])*100
        Percent.append(int(round(percentage)))

    dict.update(FindTop5(Percent,ListofSymbol))
    return dict

def Loss():
    x = collection.find()
    ListofSymbol = []
    ListOfopenPrice = []
    ListofLastPrice = []
    Percent = []
    dict = {'Symbol':'Percentage'}

    for item in x:
        ListOfopenPrice.append(float(item.get('openPrice')))
        ListofLastPrice.append(float(item.get('lastPrice')))
        ListofSymbol.append(item.get('symbol'))

    for i in range(len(ListOfopenPrice)):
        percentage = ((ListofLastPrice[i]-ListOfopenPrice[i])/ListOfopenPrice[i])*100
        Percent.append(int(round(percentage)))

    for i in range(5):
        bottom = min(Percent)
        index = Percent.index(bottom)
        symbol = ListofSymbol[index]
        dict[symbol] = abs(bottom)
        Percent.pop(index)
        ListofSymbol.pop(index)
    return dict

@app.route("/")
def Home():
    return render_template("home.html")

@app.route("/Dashboard")
def Dashboard():
    dict = Volume()
    prof = profit()
    loss = Loss()
    return render_template("chart.html", data=dict, data2=prof, data3=loss)


#APIs
@app.route("/getdata")
def getData():
    x = collection.find()
    list_cur = list(x)
    json_data = dumps(list_cur)
    return json_data

@app.route("/getDataById/<id>")
def getDataById(id):
    objId = "62eea0f59c4552db252f7a" + id
    x = collection.find_one(ObjectId(objId))
    json_data = dumps(x)
    return json_data

@app.route("/getRangeofItems/<r>")
def getRangeOfItem(r):
    range = int(r)
    x = collection.find()
    list_cur = list(x)
    json_data = dumps(list_cur[:range])
    return json_data
