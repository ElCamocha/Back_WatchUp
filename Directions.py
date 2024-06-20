from datetime import datetime, timedelta, timezone
from flask import Flask, json
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, get_jwt_identity, create_refresh_token    

from BackEnd.Directions.usersDirections import userBlueprint

from BackEnd.GlobalInfo.Keys import jwtKey

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = jwtKey
app.config["JWT_ACCES_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app) 

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            identity = get_jwt_identity()
            claims = get_jwt()
            accessToken = create_access_token(
                identity=identity, additional_claims={'strRol': claims['strRol']} if 'strRol' in claims else None
            )
            refreshToken = create_refresh_token(
                identity=identity, additional_claims={'strRol': claims['strRol']} if 'strRol' in claims else None
            )
            data = response.get_json()
            if type(data) is dict:
                data["accessToken"] = accessToken
                data["refreshToken"] = refreshToken
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response
    
app.register_blueprint(userBlueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6011, debug=True, threaded=True)