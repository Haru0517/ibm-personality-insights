from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import personal_analyzer

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


@app.route('/personal_result')
def personal_result():
    title = '診断結果'

    # 個人のデータを取得
    score_dic = personal_analyzer.analyze_personality()

    return render_template('personal_result.html', title=title, result=score_dic)


@app.route('/company_result')
def company_result():
    title = 'おすすめ企業リスト'

    # 個人のデータを取得
    company_list = {}

    return render_template('company_result.html', title=title, result=company_list)






# /post にアクセスした時の処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから名前を所得して
        name = request.form['name']

        # 個人のデータを取得
        score_dic = personal_analyzer.analyze_personality()

        # index.html をレンダリングする
        return render_template('index.html', name=score_dic['ope'], title=title)
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

