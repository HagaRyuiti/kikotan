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
        pet_id INTEGER,
        image_path TEXT,
        date DATE,
        title TEXT,
        content TEXT,
        FOREIGN KEY (pet_id) REFERENCES pets (id)
        )
    ''')

    # ペットと日記の関連テーブル
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pet_diary_relation (
        pet_id INTEGER,
        diary_id INTEGER,
        FOREIGN KEY (pet_id) REFERENCES pets (id),
        FOREIGN KEY (diary_id) REFERENCES diaries (id)
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

    return render_template('home.html', pets=pets, diaries=diaries)


@app.route('/add_pet', methods=['POST'])
def add_pet():
    image = request.files['image']
    name = request.form['petName']
    dob = request.form['dob']

    # 画像を保存するパスを生成
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

    # 画像を指定のパスに保存
    image.save(image_path)

    # データベースにペットを保存
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pets (image_path, name, dob) VALUES (?, ?, ?)', (image_path, name, dob))
    pet_id = cursor.lastrowid  # Get the ID of the newly inserted pet
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/add_diary', methods=['POST'])
def add_diary():
    image = request.files['image']
    date = request.form['date']
    title = request.form['title']
    content = request.form['content']
    pet_id = request.form['pet_id']  # Get the pet ID from the form

    # 画像を保存するパスを生成
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

    # 画像を指定のパスに保存
    image.save(image_path)

    # データベースに日記を保存
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO diaries (pet_id, image_path, date, title, content) VALUES (?, ?, ?, ?, ?)',
                   (pet_id, image_path, date, title, content))
    diary_id = cursor.lastrowid  # Get the ID of the newly inserted diary

    # ペットと日記の関連を保存
    cursor.execute('INSERT INTO pet_diary_relation (pet_id, diary_id) VALUES (?, ?)', (pet_id, diary_id))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

