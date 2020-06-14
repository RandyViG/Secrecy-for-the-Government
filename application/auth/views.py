from flask import render_template, session, redirect, flash, url_for 
from application.forms import LoginForm
from . import auth
from application.models import UserModel,UserData
from flask_login import login_user, login_required, logout_user
from application.firebase_service import get_user
#from werkzeug.security import generate_password_hash,check_password_hash

#este es el blueprint
@auth.route('/login',methods=['GET','POST'])
def login():
    login_form=LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.is_submitted():  
        user_id = login_form.username.data
        password = login_form.password.data

        user_doc = get_user( user_id )
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            if password == password_from_db:
                user_name = user_doc.to_dict()['user']
                user_data = UserData( user_id , user_name , password )
                user = UserModel( user_data )
                login_user( user )
                return redirect(url_for('index'))
            else:
                flash('Contraseña invalida')
        else:
            flash('El nombre de usuario No existe Intente de nuevo')

    return render_template('login.html',**context)
