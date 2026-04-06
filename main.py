from flask import Flask, render_template, redirect, request, flash, jsonify, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
import random
import os


from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_your_site'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


@app.route('/')
@app.route('/index')
def index():
    """Главная страница с логотипом и кнопками"""
    return render_template('index.html', title='Главная')


@app.route('/about')
def about():
    """Страница с описанием проекта"""
    return render_template('about.html', title='О проекте')

@app.route('/developers')
def developers():
    """Страница с информацией о разработчиках"""
    developers_list = [
        {
            'name': 'Лугов Святослав',
            'role': 'Автор идеи, Программист, Дизайнер игр',
            'bio': 'Всем хорошего времени суток, 8 часов сна и не прожигать дедлайны!',
            'photo': 'developer.png',  # имя файла фото
            'avatar_url': url_for('static', filename='img/developers/developer.png')
        },
        {
            'name': 'Семчик Максим',
            'role': 'Программист, Тестировщик, Дизайнер сайта',
            'bio': 'Просто хороший человек',
            'photo': 'developer.png',
            'avatar_url': url_for('static', filename='img/developers/developer.png')
        },
        {
            'name': 'Аникин Роман',
            'role': 'Программист игр',
            'bio': '- Без комментариев',
            'photo': 'developer.png',
            'avatar_url': url_for('static', filename='img/developers/developer.png')
        }
    ]
    return render_template('developers.html', title='Разработчики', developers=developers_list)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Страница обратной связи"""
    form = FeedbackForm()

    if form.validate_on_submit():
        # Здесь можно добавить отправку email или сохранение в БД
        flash('Спасибо за ваше сообщение! Мы ответим вам в ближайшее время.', 'success')
        return redirect('/feedback')

    return render_template('feedback.html', title='Обратная связь', form=form)


@app.route('/achievements')
def achievements():
    """Страница с достижениями проекта"""
    achievements_list = [
        {
            'title': 'Золотая дюжина',
            'description': 'Проект получил призовое место на конкурсе',
            'icon': '🏆',
            'year': '2026'
        },
        {
            'title': 'Активная поддержка',
            'description': 'Мы постоянно поддерживаем и развиваем проект',
            'icon': '⏰',
            'year': '2025'
        },
        {
            'title': 'Будущее достижение',
            'description': 'Это место будет занято позже',
            'icon': '🎉',
            'year': '20XX'
        },
        {
            'title': 'Будущее достижение',
            'description': 'Это место будет занято позже',
            'icon': '🎉',
            'year': '20XX'
        }
    ]
    return render_template('achievements.html', title='Наши достижения', achievements=achievements_list)


@app.route('/support')
def support():
    """Страница поддержки проекта с салютом"""
    return render_template('support.html', title='Поддержать проект')


@app.route('/api/fireworks')
def fireworks():
    """API для салюта"""
    colors = []
    for _ in range(random.randint(5, 10)):
        color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
        colors.append(color)

    return jsonify({
        'success': True,
        'colors': colors,
        'message': 'Спасибо за поддержку! 🎆'
    })


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация пользователя"""
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Такой пользователь уже есть")

        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Вход пользователя"""
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'С возвращением, {user.name}!', 'success')
            return redirect("/")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
@login_required
def logout():
    """Выход пользователя"""
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect("/")


def main():
    # Создаем папку для базы данных, если её нет
    db_dir = os.path.join(os.path.dirname(__file__), 'db')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Создана папка для базы данных: {db_dir}")

    # Используем абсолютный путь к файлу базы данных
    db_path = os.path.join(db_dir, 'blogs.db')
    print(f"Путь к базе данных: {db_path}")

    # Инициализация базы данных
    db_session.global_init(db_path)

    # Запуск приложения
    app.run(port=1007, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()