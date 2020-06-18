from application import create_app
from flask import render_template, request, redirect, url_for,flash
from flask_login import login_required, current_user,logout_user
from werkzeug.utils import secure_filename 
from Crypto.Hash import SHA256
from application.firebase_service import put_fileHash,get_hash,put_owner,get_file
from application.crypto import generate_keys, getHash, rsaOPRF
import base64
import json

app = create_app()
#app.run(ssl_context='adhoc')

generate_keys()

@app.route('/')
@login_required
def index():
    username= current_user.name
    context={
        'username':username
    }
    return render_template( 'index.html',**context )



@app.route('/keygen', methods=['GET','POST'])
@login_required
def keygen():
    if request.method == 'POST':
        k = request.json["k"]
        username= current_user.id
        context={'username':username}
        print("k:",k)
        open("./application/data/"+str(current_user.name)+".txt","w").write(k)
        return render_template( 'index.html',**context )
    return render_template( 'keygen.html')

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
        fname = secure_filename( f.filename )
        f = f.read()
        if str(f) =="b''":
            return redirect(url_for('upload_file'))
        else:
            #Convert the hash to base64
            h = getHash(f)
            z = rsaOPRF(h)
            h_fb=base64.urlsafe_b64encode( h.digest() ).decode('ascii')
            hash_doc=get_hash(hash=h_fb)
            if hash_doc.to_dict() is None: #NO EXISTE
                #Primer usuario
                put_fileHash(hash=h_fb,filename=fname,user_id=userid,username=username)
                #flash('Primer usuario')
            else:
                put_owner(hash=h_fb,user_id=userid,username=username)
                #flash('Ya estaba el hash')
            return redirect(url_for('upload_file'))
            
    return render_template( 'upload.html' ,**context)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@app.route('/prueba/recuperar')
def recuperar():
    hash = "xJGJQ16GvH7XOBLBmt8DUWZFJc15Am9EXMIzI1Hc7M0="
    dataFile = get_file(hash)
    dataFile = dataFile.to_dict()
    dataFile["nonce"] = dataFile["nonce"].replace("=","")
    dataFile["nonce"] += "AAAAAAAAAAA="
    dataFile.setdefault("key",hash)
    dataFile = json.dumps(dataFile)
    print(dataFile)
    return render_template("recuperar.html",dataFile = dataFile)

if __name__ == "__main__":
    app.run( ssl_context=('cert.pem', 'key.pem') , debug = True)