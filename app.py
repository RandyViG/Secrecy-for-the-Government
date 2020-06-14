from application import create_app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user,logout_user
from werkzeug.utils import secure_filename 
from Crypto.Hash import SHA256
import base64

app = create_app()
#app.run(ssl_context='adhoc')

@app.route('/')
@login_required
def index():
    username= current_user.id
    #print("user name: ",username)
    context={
        'username':username
    }
    return render_template( 'index.html',**context )

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload_file():
    username= current_user.id
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
            #Convert
            h = SHA256.new( )
            h.update( f )
            h_fb=base64.encodestring( h.digest() ).decode('ascii')
            return redirect(url_for('upload_file'))
    return render_template( 'upload.html' ,**context)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


if __name__ == "__main__":
    app.run( ssl_context=('cert.pem', 'key.pem') )