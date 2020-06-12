from flask_login import UserMixin
#from .firestore_service import get_user

class UserData:
    def __init__(self,username,password):
        self.username=username
        self.password=password

class UserModel(UserMixin):
    def __init__(self,user_data):
        '''
        parametros: UserData
        '''
        self.id=user_data.username
        self.password=user_data.password
    
    @staticmethod
    def query(user_id):
        #buscar user en la base de datos
        #user_doc=get_user(user_id)
        #convertirlo a user model
        user_data=UserData(
            username='Paola',
            password='Hola'
        )
        #Retornar el nuevo user model
        return UserModel(user_data)


