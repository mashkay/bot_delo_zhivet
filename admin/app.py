import os

import flask_admin
import flask_login as login
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for, request
from flask_admin import expose, helpers, AdminIndexView
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_security import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import form, fields, validators

from src.core.db.db import Base_admin
from src.core.db.model import (Assistance_disabled, Pollution,
                               Volunteer, Role, Staff, User)

load_dotenv()

app = Flask(__name__)
app.secret_key = 'xxxxyyyyyzzzzz'

app.config['FLASK_ENV'] = 'development'
app.config.from_pyfile('config.py')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}")


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_size=10000,
                       max_overflow=100)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base_admin.query = db_session.query_property()
Base_admin.metadata.create_all(engine)
Session = sessionmaker(binds={Base_admin: engine})
session = Session()


class LoginForm(form.Form):
    """Форма входа в админку"""
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(Staff).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    """Форма регистрации"""
    login = fields.StringField(validators=[validators.InputRequired()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        if db.session.query(Staff).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(staff_id):
        return db.session.query(Staff).get(staff_id)


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return (current_user.is_active
                and current_user.is_authenticated
                and current_user.has_role('admin'))


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for(
            '.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = Staff()

            form.populate_obj(user)
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for(
            '.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


@app.route('/')
def index():
    return render_template('index.html')


init_login()


admin = flask_admin.Admin(app, 'Example: Auth', index_view=MyAdminIndexView(),
                          base_template='my_master.html',
                          template_mode='bootstrap4')

if Staff.query.filter_by(login='admin').all():
    admin.add_view(MyModelView(Staff, db.session, name='Staff'))
if not Staff.query.filter_by(login='admin').all():
    admin.add_view(ModelView(Staff, db.session, name='Staff'))

admin.add_view(MyModelView(Role, db.session, name='Role'))
admin.add_view(MyModelView(User, db.session, name='User'))
admin.add_view(MyModelView(Volunteer, db.session, name='Volunteer'))
admin.add_view(MyModelView(Pollution, db.session, name='Pollution'))
admin.add_view(
    MyModelView(Assistance_disabled, db.session, name='Assistance_disabled')
)


def build_sample_db():
    admin_role = Role(name='admin', description='admin')
    db.session.add(admin_role)
    db.session.commit()


if __name__ == '__main__':
    if not Role.query.filter_by(name='admin').all():
        with app.app_context():
            build_sample_db()
    app.run(debug=True)