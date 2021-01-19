from flask import Flask, jsonify
from flask_restful import Api, Resource, request, abort, marshal_with, reqparse, fields
from flask_sqlalchemy import SQLAlchemy, Model
from passlib.apps import custom_app_context as pwd_context
import datetime 

app = Flask(__name__)
app.config.from_object('config.DevConfig')
api = Api(app)
db = SQLAlchemy(app)
post_parser = reqparse.RequestParser()

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index = True)
    email = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    __table_args__ = (db.UniqueConstraint('id', 'username'),)

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
    def __repr__(self):
        return f"id: {id}, username: {username}, email: {email}"

db.drop_all()
db.create_all()



class GetLoggedUserInfo(Resource):
    def get(self, session_id):
        usr = UserModel.query.filter_by(id = session_id).first()    
        if usr is not None:
            return {
                "username" : usr.username
            }
        else: 
            return {
                "username": 'usuario invalido'
            }, 400

class AuthenticationCreateUser(Resource):
    def post(self):
        post_parser.add_argument('username', type=str,)
        post_parser.add_argument('password', type=str,)
        args = post_parser.parse_args()

        username = args.username
        password = args.password
        if username is None or password is None or username == "" or password == "":
            return {"results" : {
            "message" : "Preencha os campos de login e senha!"
            } 
        }, 400
        if UserModel.query.filter_by(username = username).first() is not None:
            return {"results" : {
            "message" : "Usuário já existe!"
            } 
        }, 200
            abort(400) # existing user
        user = UserModel(username = username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return {"results" : {
                "message" : "Conta criada com sucesso!"
            } 
        }, 200

class Authentication(Resource):
    def post(self): 
        post_parser.add_argument('username', type=str,)
        post_parser.add_argument('password', type=str,)
        args = post_parser.parse_args()
        username = args.username
        password = args.password
        user = UserModel.query.filter_by(username = username).first()
        if user is not None:
            if user.verify_password(password):
                return {
                    "message" : "Usuario logado com sucesso!",   
                    "session_id" : user.id,
                }, 200
            else:
                return {
                    "message" : "Senha incorreta"   
                }, 401
        else:
            return {
            "message" : "Usuario inexistente"   
            }, 400

class HelloWorld(Resource):
    def get(self):
        
        return {"data" : {
         "message" : "Hello World"   
        }}

api.add_resource(Authentication, "/auth")
api.add_resource(HelloWorld, "/helloworld")
api.add_resource(AuthenticationCreateUser, "/authentication-create-user")
api.add_resource(GetLoggedUserInfo, "/usr/<int:session_id>")


if __name__ == "__main__":
    app.run(debug=True, port=6000)
