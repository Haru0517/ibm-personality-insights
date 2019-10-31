from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from personal_analyzer import analyze_personality
from big_five_graph import make_big_five_graph
from company_recommender import get_recommended_companies, print_json_list
from utils import write_to_json, load_json

app = Flask(__name__)


dummy_dic0 = {
    "ope": 0,
    "con": 0,
    "ext": 0,
    "agr": 0,
    "emo": 0
}

dummy_dic1 = {
    "ope": 1,
    "con": 1,
    "ext": 1,
    "agr": 1,
    "emo": 1
}


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

    # 個人のデータを保存
    write_to_json(target_dic, 'json/target.json')

    # 画像を作成
    image_path = 'images/target.png'
    make_big_five_graph([target_dic, dummy_dic0, dummy_dic0, dummy_dic1], image_path)

    return render_template('personal_result.html', title=title, result=score_dic)


@app.route('/company_result')
def company_result():
    title = 'おすすめ企業リスト'

    # 個人のデータを取得
    target_dic = load_json('json/target.json')

    # おすすめ企業のデータを取得
    companies = get_recommended_companies(target_dic)

    # 個人と各企業のパラメータを重ねた画像を作成
    for company in companies:
        image_path = 'images/{0}.png'.format(company['id'])
        com_param_dic = company['params']
        make_big_five_graph([target_dic, com_param_dic, dummy_dic0, dummy_dic1], image_path)

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

