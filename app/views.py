# -*- Mode: Python; coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, flash, jsonify
from app import app, db
from sqlalchemy.sql import or_
from flask_admin.model.template import macro
import os, json
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Extrato, Cadastro, AdminUser
from app.forms import LoginForm, CadastroForm, SolicitarCadastroForm
from flask_restful import Resource, Api
# from app.admin.MyAdminIndexView import login_view
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import func
# import bcrypt

# salt = bcrypt.gensalt()
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

# class User(UserMixin):
# 	pass


# @login_manager.user_loader
# def user_loader(email):
# 	lista = Users.query.filter_by(email_id=email).first()
# 	if email == False:
# 		return
# 	user = User()
# 	user.id = email
# 	return user


# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	form = LoginForm(request.form)
# 	if request.method == 'GET': 
# 		return render_template('login.html')
# 	email = request.form['email']
# 	users = Users.query.filter(Users.email.has(email=email)).first()
# 	if users and check_password_hash(users.passwd, request.form['passwd']):
# 		user = User()
# 		user.id = users
# 		login_user(user)
# 		# flash('Welcome %s' % users.id)
# 		return redirect(url_for('protected'))
# 	else:
# 		flash('Username or password incorrect.', 'error')
# 		return redirect(url_for('login'))

@app.route('/imprimir/<int:id>', methods=['GET'])
@login_required
def protected(id):
	detail = Extrato.query.filter(Extrato.nome_id==id, Extrato.parcela != Extrato.parcelas_paga).all()
	nome = [obj.nome for obj in detail]
	total = [obj.valor for obj in detail]
	valor_total = sum(total)
	# detail = [obj.to_json() for obj in Extrato.query.all()]
	# print(detail)
	# return jsonify(detail)
	# nome = Extrato.query.get(nome)
	# print(nome)
	# lista_ids = []
	# cadastro = Cadastro.query.all()
	# for obj in cadastro:
	# 	lista_ids.append(obj.id)

	#   #.order_by(self.model.nome_id)
	# query = (Extrato.query.filter(Extrato.parcela>0).group_by(Extrato.id))
	# date = []
	# l = []
	# v = []
	# for obj in query:
	# 	if obj.nome_id not in l:
	# 		l.append(obj.nome_id)
	# 		total = Extrato.query.with_entities(db.func.sum(Extrato.valor).label('total')).\
	# 	    		filter(Extrato.nome_id==obj.nome_id,\
	# 	    		Extrato.parcela>0).group_by(Extrato.nome_id).first()
	# 		tes = {'nome_id':obj.nome_id, 'nome':obj.nome, 'parcela':obj.parcela, 'loja':obj.loja, 'valor':obj.valor}
	# 		tes.update({'valor':total.total})
	# 		date.append(tes)
	# if request.method == 'GET': 
	# 	detalhe = Extrato.query.filter(Extrato.nome.in_(request.method))

	return render_template('imprimir.html', detail=detail, nome=nome, valor_total=valor_total) #"TESTE" + current_user.id 

# @api.route('/detail')
class DetailRest(Resource):
	def get(self, id):
		detail = [obj.to_json() for obj in Extrato.query.filter(Extrato.nome_id==id, Extrato.parcela>0).all()]
		# detail = [obj.to_json() for obj in Extrato.query.all()]
		# print(detail)
		return jsonify(detail)

api.add_resource(DetailRest, '/<int:id>')
# @app.route("/logout")
# @login_required
# def logout():
# 	logout_user()
# 	return redirect(url_for('login'))

# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	form = CadastroForm(request.form)
	if request.method == 'GET': 
		return render_template('cadastro.html')
	email = form.email.data 
	user_registrado = Users.query.filter(or_(Users.email_id == email)).first()
	if user_registrado:
		return "Usuario Já Cadastrado"
	id_login = Cadastro.query.filter(or_(Cadastro.email == email)).first()
	if id_login:
		if id_login.status and email == id_login.email:
			db.session.add(Users(email_id=id_login.id, passwd=generate_password_hash(request.form['passwd'])))
			db.session.commit()

			return 'Cadastro Efetuado com Sucesso! '
		else:
			return 'Usuário sem permissão de Cadastro'
	else:
		return 'Usuário sem permissão de Cadastro'

@app.route('/solicitar_cadastro', methods=['GET', 'POST'])
def solicitar_cadastro():
	form = SolicitarCadastroForm(request.form)
	if request.method == 'GET': 
		return render_template('solicitar_cadastro.html')
	email = form.email.data 
	user_registrado = Cadastro.query.filter(or_(Cadastro.email == email)).first()
	if user_registrado:
		return "Usuario Já Cadastrado"

	db.session.add(Cadastro(nome=request.form['nome'], cpf=request.form['cpf'], email=request.form['email'], fone=request.form['fone'], endereco=request.form['endereco'], ))
	db.session.commit()

	return 'Solicitação Efetuado com Sucesso! \n Aguarde a liberação'


    	# user = AdminUser()

     #        form.populate_obj(user)
     #        # we hash the users password to avoid saving it as plaintext in the db,
     #        # remove to use plain text:
     #        user.password = generate_password_hash(form.password.data)

     #        db.session.add(user)
     #        db.session.commit()

