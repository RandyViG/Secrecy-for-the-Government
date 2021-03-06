from flask_login import UserMixin
from .firebase_service import get_user

class UserData:
    def __init__( self , userid , username , password ):
        self.userid = userid
        self.username = username
        self.password = password

class UserModel(UserMixin):
    def __init__(self,user_data):
        #parametros: UserData
        self.id = user_data.userid
        self.name = user_data.username
        self.password = user_data.password
    
    @staticmethod
    def query(user_id):
        user_doc = get_user( user_id )
        user_data = UserData( user_id , user_doc.to_dict()['user'] , user_doc.to_dict()['password'] )
        
        #Retornar el nuevo user model
        return UserModel(user_data)

