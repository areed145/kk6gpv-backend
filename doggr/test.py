import pandas as pd
import numpy as np
import requests
import re
import datetime
from pymongo import MongoClient
from bson import json_util
import json

client = MongoClient('mongodb://localhost:27017/', username='kk6gpv', password='kk6gpv', authSource='admin')
db = client.petroleum
doggr = db.doggr