# -*- Mode: Python; coding: utf-8 -*-
from app import db, app
from flask_login import UserMixin
import datetime
from flask_security import UserMixin, RoleMixin


# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     addresses = db.relationship('Address', backref='person', lazy=True)

# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
#         nullable=False)
class Cadastro(db.Model):
	__tablename__="tbcadastro"
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(50), nullable=False, unique=False)
	# cpf = db.Column(db.Integer, nullable=False, unique=True)
	# email = db.Column(db.String(120), nullable=False, unique=True)
	fone = db.Column(db.String(11), nullable=False)
	# endereco = db.Column(db.String(50), nullable=False, unique=False)
	# cadastro = db.relationship('Users', backref='email', lazy=True)
	# status = db.Column(db.Boolean, default=False, nullable=False)
	def __repr__(self):
		return "%s" % (self.nome)

# class Users(db.Model, UserMixin):
# 	__tablename__ = "tbusers"

# 	id = db.Column(db.Integer, primary_key=True)
# 	# nome = db.Column(db.String(50), nullable=False, unique=False)
# 	# email = db.Column(db.String(120), nullable=False, unique=True)
# 	email_id = db.Column(db.Integer, db.ForeignKey('tbcadastro.id'), nullable=False)
# 	passwd = db.Column(db.String(64), nullable=False)

# 	def __repr__(self):
# 		return "%s" % (self.id)
	
	# def get_id(self):
	# 	return self.id

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
	data = db.Column(db.Date, default=datetime.datetime.utcnow)
	data_modificado = db.Column(db.Date, onupdate=datetime.datetime.utcnow)
	loja = db.Column(db.String(100))
	parcela = db.Column(db.String(4))
	parcelas_paga = db.Column(db.Integer(), default=0)
	valor = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
	nome_id = db.Column(db.Integer, db.ForeignKey(u'tbcadastro.id'), nullable=True, index=True)
	nome = db.relationship('Cadastro')

	def to_json(self):
		# data = self.data.strftime('%d/%m/%Y')
		json_extrato = {
						'id': self.id,
						'data': str(self.data.strftime('%d-%m-%Y')),
						'modificado': str(self.data_modificado),
						'loja': self.loja,
						'parcela': self.parcela,
						'valor': self.valor,
						'nome_id': self.nome_id,
						# 'nome':self.nome,
						}

		return json_extrato

	def __repr__(self):
		# if 
		return '%s %s %s %s %s' % (self.nome, self.data, self.loja, self.parcela, self.valor)
		
	# def get_id(self):
	# 	try:
	# 		res = db.session.query(Extrato).all()
	# 		print(res)
	# 	except Exception as e:
	# 		res = []
	# 		print(e)
	# 	finally:
	# 		db.session.close()
	# 		return res


		

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