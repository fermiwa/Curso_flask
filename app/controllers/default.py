from flask import Blueprint, render_template
from app import db
from app.models.forms import LoginForm
from app.models.tables import User

bp = Blueprint('default', __name__)

@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)
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