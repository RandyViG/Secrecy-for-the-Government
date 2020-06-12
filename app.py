from application import create_app
from flask import render_template, make_response,redirect
from flask_login import login_required

app = create_app()

@app.route('/')
@login_required
def index():
    return render_template( 'index.html' )