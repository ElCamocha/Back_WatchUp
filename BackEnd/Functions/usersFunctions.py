import threading
import time
import jwt
from datetime import datetime

from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

import BackEnd.GlobalInfo.Helpers as Helpers
import BackEnd.GlobalInfo.ResponseMessages as ResponsesMessages
from BackEnd.GlobalInfo.Keys import webUrl, jwtKey
from BackEnd.GlobalInfo.serverMail import ServerMail, verifyEmailTemplate, forgotPasswordEmailTemplate


dbConnLocal = Helpers.dbConnection()

userLoginProjection = {
    '_id': 1, 'strEmail': 1, 'strName': 1, 'strLastName': 1, 'blnVerified': 1
}

def signup(strName: str, strLastName: str, strEmail: str, strPassword: str):
    try:
        registeredUser = dbConnLocal.clUsers.find_one(
            {'strEmail': strEmail}
        )
        if registeredUser is not None:
            return ResponsesMessages.message409
        
        newUser = {
            'strEmail': strEmail,
            'strName': strName,
            'strLastName': strLastName,
            'strPassword': Helpers.passwordHash(strPassword),
            'blnVerified': False
        }
        
        newUser = Helpers.deleteBlankAttributes(newUser)
        insertResult = dbConnLocal.clUsers.insert_one(newUser)
        if insertResult.inserted_id:
            thread = threading.Thread(target=(
                lambda: sendVerificationEmail(strEmail)
            ))
            thread.start()
            user = dbConnLocal.clUsers.find_one({'_id': insertResult.inserted_id}, userLoginProjection)
            if '_id' in user:
                user['_id'] = str(user['_id'])
            identity = {'_id': user['_id']}
            accessToken = create_access_token(identity=identity)
            refreshToken = create_refresh_token(identity=identity)
            return {
                **ResponsesMessages.message200,
                'result': {'user': user},
                'accessToken': accessToken,
                'refreshToken': refreshToken,
                'exp': decode_token(accessToken)['exp']
            }
        else:
            return ResponsesMessages.message500
    except Exception:
        Helpers.PrintException()
        return ResponsesMessages.message500   
    

def login(strEmail: str, strPassword: str):
    try:
        user = dbConnLocal.clUsers.find_one(
            {'strEmail': strEmail, 'strPassword': Helpers.passwordHash(strPassword)}, 
            userLoginProjection
        ) 
        if user is None:
            return ResponsesMessages.message404
        
        if '_id' in user:
            user['_id'] = str(user['_id'])
            identity = {'_id': user['_id']} 
        accesToken = create_access_token(identity=identity)
        refreshToken = create_refresh_token(identity=identity)
        
        return {
            **ResponsesMessages.message200,
            'result': {'user': user},
            'accessToken':accesToken,
            'refreshToken': refreshToken,
            'exp': decode_token(accesToken)['exp']
        }
    except Exception:
        Helpers.PrintException()
        return ResponsesMessages.message500 
    
    
def sendVerificationEmail(strEmail: str):
    try:
        jsnData = {'strEmail': strEmail, 'now': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}
        strToken = jwt.encode(jsnData, jwtKey, algorithm='HS256')
        strSubject = 'Verifica tu cuenta de Watch Up'
        strBody = verifyEmailTemplate(f'{webUrl}/verificar-cuenta?token={strToken}')
        serverMail = ServerMail()
        serverMail.fnSendMessage(strSubject=strSubject, strBody=strBody, strToSend=strEmail)
    except Exception as exception:
        Helpers.PrintException()
        return ResponsesMessages.message500
    
def verifyAccount(strToken: str):
    try:
        decoded = jwt.decode(strToken, jwtKey, algorithms=['HS256'])
        strEmail = decoded['strEmail']
        updateResult = dbConnLocal.clUsers.update_one(
            {'strEmail': strEmail},
            {'$set': {'blnVerified': True}}
        )
        if updateResult.modified_count > 0:
            return ResponsesMessages.message200
        else:
            return ResponsesMessages.message203
    except Exception as exception:
        Helpers.PrintException()
        return ResponsesMessages.message500

        
        
    
        
            