from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)


# メッセージをランダムに表示
def picked_up():
    messages = [
        "こんにちは，あなたの名前を入力してください",
        "やあ！あなたの名前はなんですか？",
        "あなたの名前を教えてね"
    ]
    return np.random.choice(messages)

# ここからwebアプリケーション用のルーティングを記述
# indexにアクセスしたときの処理
@app.route('/')
def index():
    title = 'ようこそ'
    message = picked_up()
    # index.htmlをレンダリングする
    return render_template('index.html', message=message, title=title)

# /post にアクセスした時の処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから名前を所得して
        name = request.form['name']
        # index.html をレンダリングする
        return render_template('index.html', name=name, title=title)
    elif request.method == 'GET':
        # リクエストフォームから名前を所得して
        name = request.args.get('name', "") if request.args.get('name', "") != "" else "No name"

        # index.html をレンダリングする
        return render_template('index.html', name=name, title=title)
    else:
        # エラーなどでリダイレクトしたいとき
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True  # デバッグモードを有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に

