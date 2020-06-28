from application import create_app
from flask import render_template, request, redirect, url_for,flash, make_response, jsonify
from flask_login import login_required, current_user
from application.forms import AddUser, Setting
from werkzeug.utils import secure_filename 
from Crypto.Hash import SHA256
from application.firebase_service import put_fileHash,get_hash,put_owner,get_file,get_files,put_keyUser,delete_file,owner_exist, put_user
from application.crypto import generate_keys, getHash, rsaOPRF, aes256,rsaOAEP,get_MIME
from werkzeug.security import generate_password_hash
import base64
import binascii
import json

app = create_app()
generate_keys()

@app.route('/')
@login_required
def index():
    username= current_user.name
    files = get_files( current_user.id )
    root = True if current_user.id == '0001' else False
    context = {
        'username': username,
        'files': files,
        'root': root,
        'add_user': AddUser(),
        'settings': Setting()  
    }
    
    return render_template( 'index.html',**context )

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload_file():
    username= current_user.name
    userid=current_user.id

    if request.method == 'POST':
        if not 'file' in request.files:
            return 'No file part in the form'
        f = request.files['file']
        print(f)
        fname = secure_filename( f.filename )
    
        f = f.read()
        if str(f) =="b''": #No se subio nada
            return redirect(url_for('upload_file'))
        else:
            #Convert the hash to base64
            h = getHash(f)
            h_fb=base64.urlsafe_b64encode( h.digest() ).decode('ascii')
            hash_doc=get_hash(hash=h_fb)
            Gz = rsaOPRF( h )
            if Gz is None:
                username= current_user.name
                files = get_files( current_user.id )
                root = True if current_user.id == '0001' else False
                band= True
                context = {
                    'username': username,
                    'files': files,
                    'root': root,
                    'add_user': AddUser(),
                    'settings': Setting(),  
                    'band': band
                }
                return render_template( 'index.html',**context )
                
            if hash_doc.to_dict() is None: #NO EXISTE
                #Primer usuario      
                nonce,encryptFile = aes256(h=Gz,f=f)
                #Hexadecimal
                encryptFile_hexa = binascii.hexlify( encryptFile )
                y = str( encryptFile_hexa,'ascii' )
                nonce_hexa = binascii.hexlify( nonce )
                nonce_hexa = str(nonce_hexa,'ascii')
                put_fileHash(hash=h_fb,filename=fname,user_id=userid,username=username,encryptFile=y,nonce=nonce_hexa)
                
                #flash('Primer usuario')
            else:
                if owner_exist(hash=h_fb,user_id=userid):
                    flash('El archivo '+fname+' ya existe.')
                    return redirect(url_for('upload_file'))
                else:
                    put_owner(hash=h_fb,user_id=userid,username=username)
                #flash('Ya estaba el hash')
            #flash(base64.b64encode(Gz))
            public_key_user = open('application/data/'+userid+'.pem').read()
            Gz_cipher = rsaOAEP( Gz,public_key_user )
            
            #base64
            Gz_cipher = base64.urlsafe_b64encode(Gz_cipher).decode('ascii')
            put_keyUser(user_id=userid,filename=fname,h=Gz_cipher,id_hash=h_fb)

            return redirect(url_for('upload_file'))
            
    return redirect(url_for('index'))

@app.route('/delete/<file>')
def delete(file):
    user_id = current_user.id
    delete_file( user_id , file )
    flash('Archivo: {}  borrado'.format(file) )

    return redirect(url_for('index'))


@app.route('/download', methods=['GET','POST'])
@login_required
def download():
    if request.method == 'POST':
        file = request.json["file"]
        print("nombre:",file)
        user_id = current_user.id
        hash,data_file = get_file(user_id,file)
        #Coreccion base64 urlsafe
        hash=hash.replace('-','+').replace('_','/')
        data_file.setdefault("hash",hash)
        data_file.setdefault("mime",str(get_MIME(data_file["filename"])))

        return jsonify(result = data_file)

@app.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    user_id = current_user.id
    settings_form = Setting()
    if settings_form.is_submitted():
        username = settings_form.username.data
        password = settings_form.password.data
        password_hash = generate_password_hash( password )
        put_user( user_id , username , password_hash )
        flash('Tus cambios se realizaron con éxito')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run( ssl_context=('cert.pem', 'key.pem') , debug = True)