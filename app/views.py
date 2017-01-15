# -*- Mode: Python; coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, flash
from app import app, db
from sqlalchemy.sql import or_
import os
from werkzeug import check_password_hash, generate_password_hash
from app.models import Users, Extrato, Cadastro
from app.forms import LoginForm, CadastroForm, SolicitarCadastroForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# import bcrypt

# salt = bcrypt.gensalt()


login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
	pass


@login_manager.user_loader
def user_loader(email):
	lista = Users.query.filter_by(email=email).first()
	if email == False:
		return
	user = User()
   	user.id = email
   	return user


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'GET': 
		return render_template('login.html')
	email = request.form['email']
	users = Users.query.filter_by(email=email).first()
	if users and check_password_hash(users.passwd, request.form['passwd']):
		user = User()
		user.id = users
		login_user(user)
		# flash('Welcome %s' % users.id)
		return redirect(url_for('protected'))
	else:
		flash('Username or password incorrect.', 'error')
		return redirect(url_for('login'))
	
	
@app.route('/protected')
@login_required
def protected():
	nome = Users.query.get(current_user.id)
	testes = Extrato.query.filter(Extrato.users_id == current_user.id).all()
	return render_template('base.html', testes=testes, nome=nome) #"TESTE" + current_user.id 

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	form = CadastroForm(request.form)
	if request.method == 'GET': 
		return render_template('cadastro.html')
	email = form.email.data 
	user_registrado = Users.query.filter(or_(Users.email == email)).first()
	if user_registrado:
		return "Usuario Já Cadastrado"

	if Cadastro.query.filter(or_(Cadastro.email == email)).first():
		db.session.add(Users(nome=request.form['nome'], email=request.form['email'], passwd=generate_password_hash(request.form['passwd'])))
		db.session.commit()

		return 'Cadastro Efetuado com Sucesso!'

	return 'Usuário sem permissão de cadastro'

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

	return 'Cadastro Efetuado com Sucesso!'


    	# user = AdminUser()

     #        form.populate_obj(user)
     #        # we hash the users password to avoid saving it as plaintext in the db,
     #        # remove to use plain text:
     #        user.password = generate_password_hash(form.password.data)

     #        db.session.add(user)
     #        db.session.commit()

