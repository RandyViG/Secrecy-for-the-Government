from flask_login import UserMixin
from .firebase_service import get_user
#from .firestore_service import get_user
user={
    'Pao': 'Paola',
    'Ran': 'Randy',
    'Bran': 'Brandon'
}

class UserData:
    def __init__(self,username,password):
        self.username = username
        self.password = password

class UserModel(UserMixin):
    def __init__(self,user_data):
        #parametros: UserData
        self.id = user_data.username
        self.password = user_data.password
    
    @staticmethod
    def query(user_id):
        user_doc = get_user( user_id )
        user_data = UserData( user_doc.to_dict()['user'] , user_doc.to_dict()['password'] )
        #Retornar el nuevo user model
        return UserModel(user_data)

