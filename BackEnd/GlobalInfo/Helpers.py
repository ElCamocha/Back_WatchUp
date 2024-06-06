import jwt
import hashlib
import json
import datetime
import sys
import time
import linecache

from pymongo import MongoClient
from pytz import timezone
from datetime import datetime

import BackEnd.GlobalInfo.Keys as connectKeys

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

def dbConnection():
    if connectKeys.dbConn is None:
        mongoConnect = MongoClient(connectKeys.mongoUrl)
        connectKeys.dbConn = mongoConnect['watchUp']
    return connectKeys.dbConn


def passwordHash(strPassword):
    hashed = hashlib.sha256(bytes(strPassword, 'utf-8')).hexdigest()
    return hashed

def getTimestamp(dateTime: datetime= datetime.utcnow()):
    now = time.mktime(dateTime.timetuple())
    return int(now)

def createJWT(body):
    return jwt.encode(body, connectKeys.jwtKey, algorithm='HS256')

def deleteBlankAttributes(directory):
    newDirectory = {}
    for attribute in directory:
        if directory[attribute] != "":
            newDirectory = {
                **newDirectory,
                attribute: directory[attribute]
            }
    return newDirectory
   
