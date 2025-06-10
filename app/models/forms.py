from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.tables import User


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class RegisterForm(FlaskForm):
    username = StringField("Usuária", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    confirm_password = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    name = StringField("Nome", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este usuário já existe. Digite outro!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Uma conta já foi criada com esse e-mail. Use um e-mail diferente!')
