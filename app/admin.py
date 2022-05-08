# -*- Mode: Python; coding: utf-8 -*-
from re import template
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template, redirect, url_for, Blueprint, request
from .models import Extrato, AdminUser, Cadastro
from app import db, sqla
import flask_admin as admin
from app.forms import LoginFormAdmin, CadastroForm
from flask_security import Security, SQLAlchemyUserDatastore
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_admin import helpers, expose
from flask_admin.actions import action
from sqlalchemy import func

admin_ = Blueprint('admin_',__name__)

from app import app
class UsersAdmin(ModelView):
    column_list = ('nome', 'email')
    column_sortable_list = ('nome')

class ExtratoAdmin(ModelView):
    column_searchable_list = [Cadastro.nome]
    column_filters = ['nome', 'loja']
    login_manager = LoginManager()
    login_manager.init_app(app)
        # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(user_id)
    def is_accessible(self):
        return current_user.is_authenticated

    def get_query(self):
        queryset = self.session.query(self.model).filter(self.model.parcela != self.model.parcelas_paga).order_by(self.model.nome_id)
    #     for obj in queryset:
    #         # filtro = self.session.query.with_entities(func.sum(self.model.valor).label('total')).first().total
    #         filtro = Extrato.query.with_entities(db.func.sum(Extrato.valor)).filter(Extrato.nome == obj.nome, Extrato.parcela>0)
    #     if filtro:   
    #         return queryset
    #     else:
        return queryset
        
    @action(
        'Print',
        'Pg parcela',
        'Tem certeza?'
    )
    def pg_parcela(self, ids):
        queryset = Extrato.query.filter(Extrato.id.in_(ids)).all()
        # print(queryset)
        try:
            for extrato in Extrato.query.filter(Extrato.id.in_(ids)).all():
                # extrato.parcela = int(extrato.parcela) - 1
                extrato.parcelas_paga = int(extrato.parcelas_paga) + 1
            db.session.commit()

        except:
            print('NAO')
    

class MyModelView(sqla.ModelView):
    # def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)
        # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(user_id)
    def is_accessible(self):
        return current_user.is_authenticated



# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    # Initialize flask-login
    
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        query = (Extrato.query.filter(Extrato.parcela != Extrato.parcelas_paga).group_by(Extrato.id))

        date = []
        l = []
        v = []
        for obj in query:
            if obj.nome_id not in l:
                l.append(obj.nome_id)
                total = Extrato.query.with_entities(db.func.sum(Extrato.valor).label('total')).\
                        filter(Extrato.nome_id==obj.nome_id,\
                        Extrato.parcela != Extrato.parcelas_paga).group_by(Extrato.nome_id).first()
                tes = {'nome_id':obj.nome_id, 'nome':obj.nome, 'loja':obj.loja, 'valor':obj.valor}
                tes.update({'valor':total.total})
                date.append(tes)
                
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
        form = AdminUser(request.form)
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

@app.context_processor
def inject_paths():
    query = (Extrato.query.filter(Extrato.parcela != Extrato.parcelas_paga).group_by(Extrato.id))
    date = []
    l = []
    v = []
    for obj in query:
        if obj.nome_id not in l:
            l.append(obj.nome_id)
            total = Extrato.query.with_entities(db.func.sum(Extrato.valor).label('total')).\
                    filter(Extrato.nome_id==obj.nome_id,\
                    Extrato.parcela != Extrato.parcelas_paga).group_by(Extrato.nome_id).first()
            tes = {'nome_id':obj.nome_id, 'nome':obj.nome, 'parcela':obj.parcela, 'loja':obj.loja, 'valor':obj.valor}
            tes.update({'valor':total.total})
            date.append(tes)
    
    # you will be able to access {{ path1 }} and {{ path2 }} in templates
    return dict(query=date)

admin = admin.Admin(app, 'Perereca Banks', index_view=MyAdminIndexView(), template_mode='bootstrap3', base_template='my_master.html')

# admin.add_view(MyModelView(Users, db.session))
admin.add_view(ExtratoAdmin(Extrato, db.session))
admin.add_view(MyModelView(Cadastro, db.session))

# Add model views
# admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(AdminUser, db.session))

# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         h=admin_helpers,
#     )