from flask import Flask, render_template, request, redirect, url_for
import sqlite3

DATABASE = 'database.db'
app = Flask(__name__)

# データベーステーブルの作成
def create_table():
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            name TEXT,
            dob TEXT,
            image TEXT
        )
    ''')

    con.commit()
    cursor.close()
    con.close()

# メインページのコード
@app.route('/')
def index():
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()

    db_pets = cursor.execute('SELECT * FROM pets').fetchall()

    cursor.close()
    con.close()

    pets = []
    for row in db_pets:
        pets.append({'name': row[0], 'dob': row[1], 'image': row[2]})

    return render_template(
        'index.html',
        pets=pets
    )

# フォーム表示のコード
@app.route('/sample')  # 'sample'エンドポイントを追加
def sample():
    return render_template(
        'sample.html'
    )  # 'sample.html'を表示

# 登録処理のコード
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    dob = request.form['dob']
    image = request.form['image']

    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO pets VALUES(?, ?, ?)',
                [name, dob, image])
    con.commit()
    con.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    # アプリ実行前にテーブル作成
    create_table()
    # アプリ実行
    app.run()