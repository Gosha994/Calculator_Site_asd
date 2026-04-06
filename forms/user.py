from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = EmailField('Ваш email', validators=[DataRequired(), Email()])
    subject = StringField('Тема', validators=[DataRequired()])
    message = TextAreaField('Сообщение', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Отправить')