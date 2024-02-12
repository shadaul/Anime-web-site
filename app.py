from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Функция для установки соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверяем, что пользователь с таким именем не существует
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return 'User with this username already exists!'

        # Создаем нового пользователя
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

# Вход пользователя
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Получаем пользователя с указанным именем
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return 'Logged in successfully!'
        else:
            return 'Login failed. Check your username and password.'

if __name__ == '__main__':
    app.run(debug=True)
