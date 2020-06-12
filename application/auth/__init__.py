from flask import Blueprint

auth= Blueprint('auth',__name__,url_prefix='/auth')

#crear una nueva vista
from . import views
