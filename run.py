
from flask import Flask
from app import api_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from Models import db, RevokedTokenModel
from Packages.auth.Authentication import mail
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix='/api')

    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)
    mail.init_app(app)
    CORS(app)
    return app
    
    

if __name__ == "__main__":
    app = create_app("config")
    app.run(host='0.0.0.0',port =9106,debug=True,ssl_context=('/etc/letsencrypt/live/graal.ens-lyon.fr/cert.pem','/etc/letsencrypt/live/graal.ens-lyon.fr/privkey.pem'))