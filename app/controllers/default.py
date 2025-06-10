from flask import Blueprint, flash, redirect, render_template, url_for
from app import db, lm
from app.models.forms import LoginForm, RegisterForm
from app.models.tables import User
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('default', __name__)

'''@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()'''

@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # Este bloco só é executado quando o formulário é SUBMETIDO (POST)
         #filtra pelo nome do usuário
        user = User.query.filter_by(username=form.username.data).first()

        #se usuário existe e senha correta
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success') 
            return redirect(url_for("default.index"))
        else:
            #se o usuário não foi encontrado ou a senha está incorreta
            flash("Usuário ou senha inválidos.", 'danger')
    return render_template('login.html', form=form)

@bp.route('/teste/<info>')
@bp.route('/teste', defaults={"info":None})
def teste(info):

    #para adicionar
    '''i = User("fertanaka", "fer123", "fernanda", "fer@gmail.com")
    db.session.add(i)
    db.session.commit()
    return "OK"'''    

    #para deletar
    '''r = User.query.filter_by(username="maria").first()
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
    flash("Logged out, 'info")
    return redirect(url_for("default.index"))

@bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Hash da senha antes de salvar no banco de dados
            hashed_password = generate_password_hash(form.password.data)

            new_user = User(
                username=form.username.data,
                password=hashed_password, # Salve a senha HASHED
                name=form.name.data,
                email=form.email.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Sua conta foi criada! Faça login.', 'success')
            return redirect(url_for('default.login'))
        except Exception as e:
            db.session.rollback() # Em caso de erro, desfaça a transação
            flash(f'Um erro aconteceu: {e}', 'danger') # Mostre o erro para depuração
            print(f"Erro no cadastro: {e}") # Log para o console

    # Se o formulário não for validado ou for um GET request
    return render_template('register.html', form=form)