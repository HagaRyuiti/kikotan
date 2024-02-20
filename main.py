from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# データベースの初期化
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 初期化関数を実行
init_db()

# 画像を保存するフォルダの指定
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ルートページ
@app.route('/')
def index():
    # データベースからデータを取得
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM uploads')
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

# 画像のアップロード処理
@app.route('/upload', methods=['POST'])
def upload():
    # フォームからテキストと画像を取得
    text = request.form['text']
    image = request.files['image']

    # 画像を保存するパスを生成
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

    # 画像を指定のパスに保存
    image.save(image_path)

    # データベースに保存
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO uploads (text, image_path) VALUES (?, ?)', (text, image_path))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
