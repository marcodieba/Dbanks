# -*- Mode: Python; coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import form, BooleanField, fields, validators, StringField, PasswordField, Form, BooleanField					
from app.models import AdminUser, Cadastro
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class LoginForm(form.Form):
	email = fields.StringField('Email', validators=[validators.DataRequired()])
	passwd = fields.PasswordField('Password', validators=[validators.DataRequired()])

class CadastroForm(form.Form):
	nome = fields.StringField('Nome', validators=[validators.DataRequired()])
	email = fields.StringField('Email', validators=[validators.DataRequired()])
	passwd = PasswordField('Password', validators=[
												validators.DataRequired(),
												validators.EqualTo('confirm', message='Passwords must match')
												])
	confirm = PasswordField('Repeat Password')

class SolicitarCadastroForm(form.Form):
    nome = fields.StringField('Nome', validators=[validators.DataRequired()])
    cpf = fields.StringField('CPF', validators=[validators.DataRequired()])
    email = fields.StringField('Email', validators=[validators.DataRequired()])
    endereco = fields.StringField('Endereco', validators=[validators.DataRequired()])
    fone = fields.StringField('Fone', validators=[validators.DataRequired()])

# Define login and registration forms (for flask-login)
class LoginFormAdmin(FlaskForm):
    login = fields.StringField(validators=[validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(AdminUser).filter_by(login=self.login.data).first()


class ExtratoForm(form.Form):
    data = fields.StringField('Nome', validators=[validators.DataRequired()])
    loja = fields.StringField('CPF', validators=[validators.DataRequired()])
    parcela = fields.StringField('Email', validators=[validators.DataRequired()])
    valor = fields.StringField('Endereco', validators=[validators.DataRequired()])
    fone = fields.StringField('Fone', validators=[validators.DataRequired()])

    