from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from personal_analyzer import analyze_personality
from company_recommender import get_recommended_companies, print_json_list
from utils import write_to_json, load_json

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
    score_dic = analyze_personality()
    target_dic = score_dic
    write_to_json(target_dic, 'json/target.json')

    return render_template('personal_result.html', title=title, result=score_dic)


@app.route('/company_result')
def company_result():
    title = 'おすすめ企業リスト'

    # 個人のデータを取得
    target_dic = load_json('json/target.json')

    # おすすめ企業のデータを取得
    companies = get_recommended_companies(target_dic)

    return render_template('company_result.html', title=title, companies=companies)






# /post にアクセスした時の処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから名前を所得して
        name = request.form['name']

        # 個人のデータを取得
        score_dic = analyze_personality()

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

