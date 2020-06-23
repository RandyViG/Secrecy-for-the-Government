import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from flask import flash
'''
cert = "C:\\Users\\nahomi\\Documents\\ESCOM\\6toSemestre\\Criptografía\\Proyecto\\FinalProjectCrypto-b9b9bfcf0fa8.json"
json_data = ""
with open(cert) as json_file:
    json_data = json.load(json_file)
cred = credentials.Certificate(json_data)
'''
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def put_keyUser(user_id,filename,h,id_hash):
    ref = db.collection('users').document(user_id).collection('keys').document(filename)
    ref.set({'hash':h,'id_hash':id_hash})

def put_fileHash(hash,filename,user_id,username,encryptFile,nonce):
    fileHash_ref = db.collection('files').document(hash).collection('owners')
    fileHash_ref.add({user_id:username})
    db.document('files/{}'.format(hash,)).set({'filename':filename,'file':encryptFile,'nonce':nonce})

def get_hash(hash):
    return db.collection('files').document(hash).get()

def put_owner(hash,user_id,username):
    hash_ref = db.collection('files').document(hash).collection('owners')
    hash_ref.add({user_id:username}) 

def get_file(user_id,filename):
    file_data = db.collection('users').document(user_id).collection('keys').document(filename).get().to_dict()
    return file_data['hash'],db.collection('files').document(file_data['id_hash']).get().to_dict()

def get_files( user_id ):
    nameFile = [ ]
    files = db.collection('files').stream()
    for file in files:  
        owners = db.collection( 'files/{}/owners'.format(file.id) ).stream()
        for owner in owners:
            try:
                owner.to_dict()[user_id]
                nameFile.append( file.to_dict()['filename'] )
                break
            except:
                continue

    return nameFile

def delete_file( user_id , file_name ):
    files = db.collection('files').stream()
    for file in files:
        if file_name == file.to_dict()['filename']:
            owners = db.collection( 'files/{}/owners'.format(file.id) ).stream()
            cont = 0
            id = 0
            for owner in owners:
                cont += 1
                try:
                    owner.to_dict()[user_id]
                    id = owner.id
                except:
                    continue
            if cont > 1 :
                db.document( 'files/{}/owners/{}'.format(file.id,id) ).delete()
            else:
                db.document( 'files/{}'.format(file.id) ).delete()
            break

