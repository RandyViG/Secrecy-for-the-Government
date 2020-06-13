from application import create_app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user,logout_user
from werkzeug.utils import secure_filename 


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
    if request.method == 'POST':
        if not 'file' in request.files:
            return 'No file part in the form'
        f = request.files['file']
        if f.filename == "":
            return 'No file selected.'
        if f:
            filename = secure_filename(f.filename)
            return 'file: ' + filename
        
        return "File not allowed."
    return render_template( 'upload.html' )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


if __name__ == "__main__":
    app.run( ssl_context=('cert.pem', 'key.pem') )