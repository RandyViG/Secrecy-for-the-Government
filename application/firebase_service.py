import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def put_fileHash(hash,filename,user_id):
    fileHash_ref = db.collection('files').document(hash).collection('owners').document(user_id)
    
    #fileHash_ref.add({'id':user_id})
    db.document('files/{}'.format(hash,)).set({'filename':filename})
    #fileHash_ref.set({'filename':filename})
    #db.collection('file').document(hash)
    
