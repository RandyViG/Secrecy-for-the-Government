from application import create_app
from application.forms import DeleteFile, DownloadFile
from flask import render_template, request, redirect, url_for,flash, make_response, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename 
from Crypto.Hash import SHA256
from application.firebase_service import put_fileHash,get_hash,put_owner,get_file,get_files,put_keyUser,delete_file
from application.crypto import generate_keys, getHash, rsaOPRF, aes256,rsaOAEP,get_MIME
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
    delete_form = DeleteFile()
    download_form = DownloadFile()
    context={
        'username':username,
        'files':files,
        'delete_form':DeleteFile(),
        'download_form':DownloadFile(),
    }
    
    return render_template( 'index.html',**context )

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload_file():
    username= current_user.name
    userid=current_user.id
    context={
        'username':username
    }
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
            z = rsaOPRF(h)
            h_fb=base64.urlsafe_b64encode( h.digest() ).decode('ascii')
            hash_doc=get_hash(hash=h_fb)
            Gz = rsaOPRF( h )
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
                put_owner(hash=h_fb,user_id=userid,username=username)
                #flash('Ya estaba el hash')
            #flash(base64.b64encode(Gz))
            public_key_user = open('application/data/'+userid+'.pem').read()
            Gz_cipher = rsaOAEP( Gz,public_key_user )
            
            #base64
            Gz_cipher = base64.urlsafe_b64encode(Gz_cipher).decode('ascii')
            put_keyUser(user_id=userid,filename=fname,h=Gz_cipher,id_hash=h_fb)

            return redirect(url_for('upload_file'))
            
    return render_template( 'upload.html' ,**context)

@app.route('/delete/<file>')
def delete(file):
    user_id = current_user.id
    delete_file( user_id , file )

    return redirect(url_for('index'))


@app.route('/download', methods=['GET','POST'])
@login_required
def download():
    if request.method == 'POST':
        file = request.json["file"]
        print("nombre:",file)
        flash('descargando: '+ file)
        user_id = current_user.id
        hash,data_file = get_file(user_id,file)
        #Coreccion base64 urlsafe
        hash=hash.replace('-','+').replace('_','/')
        data_file.setdefault("hash",hash)
        data_file.setdefault("mime",str(get_MIME(data_file["filename"])))
        return jsonify(result = data_file)

if __name__ == "__main__":
    app.run( ssl_context=('cert.pem', 'key.pem') , debug = True)