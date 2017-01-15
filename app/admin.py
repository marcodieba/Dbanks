# -*- Mode: Python; coding: utf-8 -*-
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template, redirect, url_for, Blueprint, request
from models import Users, Extrato, AdminUser, Cadastro
from app import db, sqla
import flask_admin as admin
from app.forms import LoginFormAdmin, CadastroForm
from flask_security import Security, SQLAlchemyUserDatastore
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_admin import helpers, expose


admin_ = Blueprint('admin_',__name__)

from app import app
class UsersAdmin(ModelView):
    column_list = ('nome', 'email')
    
    # @expose('/cadastro/', methods=('GET', 'POST'))
    # def register_view(self):
    #     form = cadastroForm(request.form)
    #     if helpers.validate_form_on_submit(form):
    #         user = Users()

    #         form.populate_obj(user)
    #         # we hash the users password to avoid saving it as plaintext in the db,
    #         # remove to use plain text:
    #         user.password = generate_password_hash(form.password.data)

    #         db.session.add(user)
    #         db.session.commit()
            
    #         login_user(user)
    #         return redirect(url_for('.index'))

class ExtratoAdmin(ModelView):
    pass

# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(UserAdmin).get(user_id)

class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginFormAdmin(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = AdminUser()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))

admin = admin.Admin(app, 'Example: Auth', index_view=MyAdminIndexView(), base_template='my_master.html')

admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(Extrato, db.session))
admin.add_view(MyModelView(Cadastro, db.session))

# Add model views
# admin.add_view(MyModelView(Role, db.session))
# admin.add_view(MyModelView(AdminUser, db.session))

# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         h=admin_helpers,
#     )