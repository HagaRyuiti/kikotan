from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)

# データベースの初期化
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ペットのテーブル
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        name TEXT,
        dob DATE
        )
    ''')

    # 日記のテーブル
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        date DATE,
        title TEXT,
        content TEXT
        )
    ''')

    conn.commit()
    conn.close()

# 初期化関数を実行
init_db()

# 画像を保存するフォルダの指定
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ペット一覧を取得
    cursor.execute('SELECT * FROM pets')
    pets = cursor.fetchall()

    # 日記一覧を取得
    cursor.execute('SELECT * FROM diaries')
    diaries = cursor.fetchall()


    conn.close()

    return render_template('index.html', pets=pets, diaries=diaries)


@app.route('/add_pet', methods=['POST'])
def add_pet():
    image = request.files['image']
    name = request.form['petName']
    dob = request.form['dob']

    # 画像を保存するパスを生成
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

    # 画像を指定のパスに保存
    image.save(image_path)

    # データベースに保存
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pets (image_path, name, dob) VALUES (?, ?, ?)', (image_path, name, dob))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))


@app.route('/add_diary', methods=['POST'])
def add_diary():
        image = request.files['image']
        date = request.form['date']
        title = request.form['title']
        content = request.form['content']

        # 画像を保存するパスを生成
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

         # 画像を指定のパスに保存
        image.save(image_path)

        # データベースに保存
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO diaries (image_path, date, title, content) VALUES (?, ?, ?, ?)', (image_path, date, title, content))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)