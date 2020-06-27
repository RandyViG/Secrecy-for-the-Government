from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField('Número de Empleado',validators=[DataRequired()])
    password= PasswordField('Contraseña',validators=[DataRequired()])
    submit= SubmitField('Enviar')

class AddUser(FlaskForm):
    user_id = StringField('Número de Empleado',validators=[DataRequired()])
    username = StringField('Nombre de Empleado',validators=[DataRequired()])
    password = PasswordField('Contraseña',validators=[DataRequired()])
    submit = SubmitField('Enviar')    
