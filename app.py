from application import create_app
from flask import render_template, make_response,redirect

app = create_app()

@app.route('/')
def index():
    return render_template( 'index.html' )