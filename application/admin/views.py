from . import admin
from application.forms import AddUser,Setting
from application.firebase_service import get_users,get_user,put_user,delete_user, delete_keys, delete_files_from_user
from flask import render_template, session, redirect, flash, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from application.forms import Setting
from werkzeug.security import generate_password_hash

@admin.route('/users')
@login_required
def users():
    username = current_user.name
    root = True if current_user.id == '0001' else False
    users = get_users()
    context = {
        'username': username,
        'users': users,
        'root': root,
        'add_user': AddUser(),
        'settings': Setting()
    }

    return render_template( 'users.html',**context )

@admin.route('/delete_users/<id>',methods=['GET','POST'])
@login_required
def delete_users( id ):
    delete_user( id )
    return redirect( url_for('admin.users') )

@admin.route('/add_user',methods=['GET','POST'])
@login_required
def add_user():
    user_form = AddUser()
    if user_form.is_submitted():
        user_id = user_form.user_id.data
        user_name = user_form.username.data
        password = user_form.password.data

        user_doc = get_user( user_id )
        if user_doc.to_dict() is None:
            password_hash = generate_password_hash( password )
            put_user( user_id , user_name , password_hash )

            return redirect( url_for('admin.users') )
        else:
            flash('El usuario ya existe')

    return redirect( url_for('admin.users') )

@admin.route('/changeData/<user_id>',methods=['GET','POST'])
@login_required
def changeData(user_id):
    settings_form = Setting()
    if settings_form.is_submitted():
        username = settings_form.username.data
        password = settings_form.password.data
        password_hash = generate_password_hash( password )
        put_user( user_id , username , password_hash )
        flash('Tus cambios se realizaron con éxito')
    return redirect(url_for('admin.users'))

@admin.route('/restore')
@login_required
def restore_key():
    user_id = current_user.id
    delete_keys( user_id )
    delete_files_from_user( user_id )
    
    return render_template('keygen.html')