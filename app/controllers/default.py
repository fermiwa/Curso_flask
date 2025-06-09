from flask import Blueprint, flash, redirect, render_template, url_for
from app import db, lm
from app.models.forms import LoginForm
from app.models.tables import User
from flask_login import login_user, logout_user

bp = Blueprint('default', __name__)

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in")
            return redirect(url_for("default.index"))
    else:
        flash("Invalid login.")
    return render_template('login.html',
                           form = form)

@bp.route('/teste/<info>')
@bp.route('/teste', defaults={"info":None})
def teste(info):

    #para adicionar
    i = User("fertanaka", "fer123", "fernanda", "fer@gmail.com")
    db.session.add(i)
    db.session.commit()
    return "OK"    

    #para deletar
    '''r = User.query.filter_by(username="teste").first()
    db.session.delete(r)
    db.session.commit()
    return "OK"'''

    #para alterar
    '''r = User.query.filter_by(username="fer123").first()
    r.name = "FerTanaka"
    db.session.add(r)
    db.session.commit()
    return "OK"'''


@bp.route('/logout')
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for("default.index"))