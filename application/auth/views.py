from flask import render_template, session, redirect, flash, url_for, request
from application.forms import LoginForm
from . import auth
from application.models import UserModel,UserData
from flask_login import login_user, login_required, logout_user, current_user
from application.firebase_service import get_user, get_users
from os.path import isfile
from werkzeug.security import check_password_hash

def existKey(user_id):
    #path = '.\\application\\data' + user_id + '.txt'
    path = './application/data/' + user_id + '.pem'
    print(path)
    if isfile( path ):
        return True
    return False


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

            if check_password_hash( password_from_db , password ):
                user_name = user_doc.to_dict()['user']
                user_data = UserData( user_id , user_name , password )
                user = UserModel( user_data )
                login_user( user )
                if( not existKey(user_id) ):
                    return redirect(url_for('auth.keygen'))
                return redirect(url_for('index'))
            else:
                flash('Contraseña invalida')
        else:
            flash('El nombre de usuario No existe Intente de nuevo')

    return render_template('login.html',**context)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('auth.login'))

@auth.route('/keygen', methods=['GET','POST'])
@login_required
def keygen():
    if request.method == 'POST':
        k = request.json["k"]
        print("k:",k)
        with open("./application/data/"+str(current_user.id)+".pem","w") as f:
            aux='-----BEGIN PUBLIC KEY-----\n'+k+'\n-----END PUBLIC KEY-----'
            f.write(aux)
        f.close()

    return render_template('keygen.html')

@auth.route('/users', methods=['GET','POST'])
@login_required
def users():
    username = current_user.name
    root = True if current_user.id == '0001' else False
    users = get_users()
    context={
        'username': username,
        'users':users,
        'root': root
    }

    return render_template( 'users.html',**context )