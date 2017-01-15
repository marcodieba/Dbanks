# -*- Mode: Python; coding: utf-8 -*-
from app import db, app
from flask_login import UserMixin
import datetime
from flask_security import UserMixin, RoleMixin

class Users(db.Model, UserMixin):
	__tablename__ = "tbusers"

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(50), nullable=False, unique=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	passwd = db.Column(db.String(64), nullable=False)

	def __init__(self):
	        return self.nome
	
	def __repr__(self):
		nome = self.nome
		return "%s" % (self.id)

class Cadastro(db.Model):
	__tablename__="tbcadastro"
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(50), nullable=False, unique=False)
	cpf = db.Column(db.Integer, nullable=False, unique=True)
	email = db.Column(db.String(120), nullable=False, unique=True)
	fone = db.Column(db.String(50), nullable=False, unique=False)
	endereco = db.Column(db.String(50), nullable=False, unique=False)
	def __repr__(self):
		return "%s %s" % (self.id, self.email)

# class Endereco(db.Model):
# 	__tablename__="enderecos"
	# id = db.Column(db.Integer, primary_key=True)



	# def __init__(self, cidade, rua, bairro):
	# 	self.cidade = cidade
	# 	self.rua = rua
	# 	self.bairro = bairro

class Extrato(db.Model):
	__tablename__ = "tbextrato"

	id = db.Column(db.Integer, primary_key=True)
	data = db.Column(db.Date)
	loja = db.Column(db.String(100))
	parcela = db.Column(db.String(4))
	valor = db.Column(db.Float)
	users_id = db.Column(db.Integer, db.ForeignKey(u'tbusers.id'), nullable=True, index=True)
	nome = db.relationship('Users', backref='Users')
	# users_id = db.Column(db.Integer, db.ForeignKey('tbextrato.id'))	
	# nome = db.relationship('Users', backref='extrato',
 #                                 		lazy='dynamic')
 # 	def get_id(self):
 # 		return self.id

	# def __init__(self):
	# 	return self.loja

	def __repr__(self):
		# if 
		return '%s %s %s %s' % (self.data, self.loja, self.parcela, self.valor, )	

# # Define models



# class Role(db.Model, RoleMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))

#     def __str__(self):
#         return self.name


class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    def __str__(self):
        return self.email

# Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

# roles_users = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )