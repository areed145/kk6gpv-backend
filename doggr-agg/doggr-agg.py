import numpy as np
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import time
import json

#client = MongoClient('mongodb://localhost:27017/', username='kk6gpv', password='kk6gpv', authSource='admin')
client = MongoClient('mongodb://kk6gpv:kk6gpv@mongo-mongodb-replicaset-0.mongo-mongodb-replicaset.default.svc.cluster.local,mongo-mongodb-replicaset-1.mongo-mongodb-replicaset.default.svc.cluster.local,mongo-mongodb-replicaset-2.mongo-mongodb-replicaset.default.svc.cluster.local/?replicaSet=db')
    
db = client.petroleum

def agg():
    df_prod = pd.DataFrame(list(db.doggr.aggregate([
        {'$unwind': '$prod'},
        {'$match': {'prod.oil': {'$gt': 0}}},
        {'$group': {
            '_id': {"api": "$api"},
            'api': {'$first': '$api'},
            'latitude': {'$first': '$latitude'},
            'longitude': {'$first': '$longitude'},
            'api': {'$first': '$api'},
            'oil': {'$sum': '$prod.oil'},
            'water': {'$sum': '$prod.water'},
        }}
    ])))

    records = json.loads(df_prod.T.to_json()).values()
    for record in records:
        try:
            db.prod.insert_one(record)
            print(record)
        except:
            print('dupe')
            pass

    df_inj = pd.DataFrame(list(db.doggr.aggregate([
        {'$unwind': '$inj'},
        {'$match': {'inj.wtrstm': {'$gt': 0}}},
        {'$group': {
            '_id': {"api": "$api"},
            'api': {'$first': '$api'},
            'wtrstm': {'$sum': '$inj.wtrstm'},
        }},
    ])))

    records = json.loads(df_inj.T.to_json()).values()
    for record in records:
        try:
            db.inj.insert_one(record)
            print(record)
        except:
            print('dupe')
            pass

# db.collection.aggregate([
# {$unwind:"$Entities"},
# {$group:{"_id":"$_id",
#          "Date":{$first:"$Date"},
#          "Topics":{$first:"$Topics"},
#          "EntitiesSum":{$sum:"$Entities.Sentiment.Value"}}},
# {$unwind:"$Topics"},
# {$group:{"_id":"$_id",
#          "Date":{$first:"$Date"},
#          "EntitiesSum":{$first:"$EntitiesSum"},
#          "TopicsSum":{$sum:"$Topics.Sentiment.Value"}}},
# {$project:{"_id":0,"Date":1,"EntitiesSum":1,"TopicsSum":1,
#            "indSum":{$add:["$EntitiesSum","$TopicsSum"]}}},
# {$group:{"_id":"$Date",
#          "EntitiesSentimentSum":{$sum:"$EntitiesSum"},
#          "TopicsSentimentSum":{$sum:"$TopicsSum"},
#          "netSentimentSum":{$sum:"$indSum"}}}
# ])

# df = pd.DataFrame(list(db.doggr.aggregate([
#     {'$unwind': '$prod'},
#     {'$group': {'_id': '$_id',
#                 'api': {'$first': '$api'},
#                 'inj': {'$first': '$inj'},
#                 'oil': {'$sum': '$prod.oil'},
#                 'water': {'$sum': '$prod.water'}}},
#     {'$unwind': '$inj'},
#     {'$group': {'_id': '$_id',
#                 'api': {'$first': '$api'},
#                 'oil': {'$first': '$oil'},
#                 'water': {'$first': '$water'},
#                 'wtrstm': {'$sum': '$inj.wtrstm'}}},
#     {'$project': {'_id': 1, 'api': 1, 'oil': 1, 'water': 1, 'wtrstm': 1}},
# ], allowDiskUse=True)))

# print(df)

if __name__ == '__main__':
    last_hour = datetime.now().hour - 1
    while True:
        if datetime.now().hour != last_hour:
            agg()
            last_hour = datetime.now().hour
            print('got long')
        else:
            print('skipping updates')
        time.sleep(10)
