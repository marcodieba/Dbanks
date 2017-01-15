# -*- Mode: Python; coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_admin.contrib import sqla

from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

from app import views
# from models import Role, User
from app.admin import admin_

app.register_blueprint(admin_)

# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)

# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         h=admin_helpers,
#     )

# from app.login import Entrada, Saida
# class EntradaAdmin(sqla.ModelView):
#     pass

# class SaidaAdmin(sqla.ModelView):
#     pass

# admin.add_view(EntradaAdmin(Entrada, db.session))

# admin.add_view(SaidaAdmin(Saida, db.session))
# BluePrints - Modules #
# Users Module
# from app.comercial.views import mod as usersModule
# app.register_blueprint(usersModule)

# # Exercises Module

# from app.exercises.views import mod as exercisesModule
# app.register_blueprint(exercisesModule)