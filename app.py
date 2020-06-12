from application import create_app
from flask import render_template, make_response,redirect
from flask_login import login_required, current_user

app = create_app()

@app.route('/')
@login_required
def index():
    username= current_user.id
    #print("user name: ",username)
    context={
        'username':username
    }
    return render_template( 'index.html',**context )