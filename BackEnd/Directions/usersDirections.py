from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

import BackEnd.Functions.usersFunctions as callMethod
import BackEnd.GlobalInfo.Helpers as Helpers
import BackEnd.GlobalInfo.Keys as Keys
import BackEnd.GlobalInfo.ResponseMessages as ResponseMessages

userBlueprint = Blueprint('userBlueprint', __name__, url_prefix='/api/user')

@userBlueprint.post('/signup')
def signup():
    try:
        strName = None if ('strName' not in request.json) else request.json['strName']
        strLastName = None if ('strLastName' not in request.json) else request.json['strLastName']
        strEmail = None if ('strEmail' not in request.json) else request.json['strEmail']
        strPassword = None if ('strPassword' not in request.json) else request.json['strPassword']
        
        if strName is None or strLastName is None or strEmail is None or strPassword is None:
            return ResponseMessages.message422
        
        result = callMethod.signup(strName, strLastName, strEmail, strPassword)
        return jsonify(result)
    except Exception:
        Helpers.PrintException()
        return ResponseMessages.message500
    
@userBlueprint.post('/login')
def login():
    try:
        strEmail = "" if ('strEmail' not in request.json) else request.json['strEmail']
        strPassword = "" if ('strPassword' not in request.json) else request.json['strPassword']
        
        if strEmail is None or strPassword is None:
            return ResponseMessages.message422
        
        result = callMethod.login(strEmail, strPassword)
        return jsonify(result)
    except Exception:
        Helpers.PrintException()
        return ResponseMessages.message500
    
@userBlueprint.post('/verifyAccount')
def verifyAccount():
    try:
        strToken = "" if ("strToken" not in request.json) else request.json['strToken']

        if strToken is None or strToken == '':
            return ResponseMessages.message203

        response = callMethod.verifyAccount(strToken)
        return jsonify(response)
    except Exception as exception:
        Helpers.PrintException()
        return ResponseMessages.message500