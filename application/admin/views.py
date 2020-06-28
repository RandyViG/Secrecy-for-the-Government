from . import admin
from application.forms import AddUser,Setting
from application.firebase_service import get_users,get_user,put_user,delete_user
from flask import render_template, session, redirect, flash, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
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