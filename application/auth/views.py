from flask import render_template, session, redirect, flash, url_for 
from application.forms import LoginForm
from . import auth
#from app.firestore_service import get_user,user_put
#from app.models import UserModel,UserData
from flask_login import login_user, login_required, logout_user
#from werkzeug.security import generate_password_hash,check_password_hash

#este es el blueprint
@auth.route('/login',methods=['GET','POST'])
def login():
    login_form=LoginForm()
    context={
        'login_form': login_form
    }
    user={
        'Pao': 'Paola',
        'Ran': 'Randy',
        'Bran': 'Brandon'
    }
    
    if login_form.validate_on_submit():
        
        username=login_form.username.data
        password=login_form.password.data
        try:
            aux_password = user[username]
            if( aux_password == password ):
                flash('Si funciono xd')
                return redirect(url_for('index'))
            else:
                #print('Error contraseña no valida')
                flash('Contraseña invalida')
        except KeyError:
            flash('Usuario no valido')
    '''
        #Validar que el usario eixste en la bd
        user_doc=get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db=user_doc.to_dict()['password']
            if check_password_hash(password_from_db, password):
            #if password == password_from_db:
                #hacemos login del usuario
                user_data=UserData(username,password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('La informacion ingresada no coincide, intentelo de nuevo')
        else:
            flash('El usuario NO existe')

        #flash('Nombre de usuario registrado con exito')
        return redirect(url_for('index'))
    '''
    return render_template('login.html',**context)
