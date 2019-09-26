import numpy as np
import pandas as pd
from pymongo import MongoClient
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/',
                     username='kk6gpv', password='kk6gpv', authSource='admin')

db = client.petroleum

# df = pd.DataFrame(list(db.doggr.aggregate([
#     {'$unwind': '$prod'},
#     {'$match': {'prod.oil': {'$gt': 0}}},
#     {'$group': {
#         '_id': {"api": "$api"},
#         'api': {'$first': '$api'},
#         'oil': {'$sum': '$prod.oil'},
#         'water': {'$sum': '$prod.water'},
#     }}
# ])))

# df = pd.DataFrame(list(db.doggr.aggregate([
#     {'$unwind': '$inj'},
#     {'$match': {'inj.wtrstm': {'$gt': 0}}},
#     {'$group': {
#         '_id': {"api": "$api"},
#         'api': {'$first': '$api'},
#         'wtrstm': {'$sum': '$inj.wtrstm'},
#     }},
# ])))

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
