import threading
import time
import jwt

from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

import BackEnd.GlobalInfo.Helpers as Helpers
import BackEnd.GlobalInfo.ResponseMessages as ResponsesMessages
from BackEnd.GlobalInfo.Keys import webUrl, jwtKey


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
        insertUser = dbConnLocal.clUsers.insert_one(newUser)
        if insertUser.inserted_id:
            # Activar cuando se tenga la funcion de verificar email
            
            #thread = threading.Thread(target=(
            #    lambda: 
            #))
            #thread.start()
            
            user = dbConnLocal.clUser.find_one({'_id': insertUser.inserted_id}, userLoginProjection)
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
        
    
        
            