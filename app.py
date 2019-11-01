from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from personal_analyzer import analyze_personality
from big_five_graph import make_big_five_graph
from company_recommender import get_recommended_companies, print_json_list
from utils import write_to_json, load_json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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


# ここからwebアプリケーション用のルーティングを記述
# indexにアクセスしたときの処理
@app.route('/')
def index():
    title = 'Workers'
    return render_template('index.html', title=title)


@app.route('/company_result')
def company_result():
    title = 'マッチ度ランキング | Workers'

    # 個人のデータを取得
    target_dic = analyze_personality()

    # 個人のデータを保存
    write_to_json(target_dic, 'json/target.json')

    # おすすめ企業のデータを取得
    companies = get_recommended_companies(target_dic)

    # 個人と各企業のパラメータを重ねた画像を作成
    for company in companies:
        image_path = 'static/images/{0}.png'.format(company['id'])
        com_param_dic = company['params']
        make_big_five_graph([target_dic, com_param_dic, dummy_dic0, dummy_dic1], image_path)

    return render_template('company_result.html', title=title, companies=companies)


@app.route('/personal_result')
def personal_result():
    title = '診断結果 | Workers'

    # 個人のデータを取得
    target_dic = load_json('json/target.json')

    # 画像を作成
    image_path = 'static/images/target.png'
    make_big_five_graph([target_dic, dummy_dic0, dummy_dic0, dummy_dic1], image_path)

    return render_template('personal_result.html', title=title, result=target_dic)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.debug = True  # デバッグモードを有効化
    app.run(host='localhost')  # どこからでもアクセス可能に

