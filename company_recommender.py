import json
from typing import List


def load_json(filepath):
    """"""
    with open(filepath, 'r') as f:
     json_data = json.load(f)
    print(json_data)
    return json_data


def print_json_list(json_list):
    for json_data in json_list:
        print(json.dumps(json_data, indent=4))


def calc_similarity(target_dic: dict, employee_dic: dict):
    """個人と企業の類似度を算出する．

    Args:
        target_dic (dict): 個人のパラメータ．
        employee_dic (dict): 企業のパラメータ．

    Returns:
        float: 類似度．（ユークリッド距離の逆数）
    """

    keys = list(target_dic.keys())

    ibm_profession = 0
    for key in keys:
        ibm_profession += (abs(target_dic[key]-employee_dic[key]))

    precision_profession = (1/(1+ibm_profession))*100

    return precision_profession


def get_recommended_companies(target_dic):
    """類似度が高い順にソートして返す．

    Args:
        target_dic (dict): 個人の診断結果．

    Returns:
        List[dict]: 類似度を含んだソート済みの企業データリスト．
    """
    #  jsonを読み込んで企業リストを取得
    company_list = load_json('json/company.json')

    # 企業ごとに類似度を計算
    ret_company_list = []
    for company in company_list:
        sim = calc_similarity(target_dic, company['params'])
        company['similarity'] = sim
        ret_company_list += [company]

    # ソートして返す
    ret_company_list = sorted(ret_company_list, key=lambda x: x['similarity'], reverse=True)
    print(ret_company_list)

    return ret_company_list


if __name__ == '__main__':
    target_dic = {'ope': 0.8243266441684023, 'con': 0.633414931260427, 'ext': 0.8117213140033163, 'agr': 0.676611520481196, 'emo': 0.5190227982392853}

    employee_dic1 = {'ope': 0.8143266441684023, 'con': 0.623414931260427, 'ext': 0.8017213140033163, 'agr': 0.66611520481196, 'emo': 0.5090227982392853}

    employee_dic2 = {'ope': 0.5555555555555555, 'con': 0.633414931260427, 'ext': 0.9999999999, 'agr': 0.99999999999, 'emo': 0.1111111111111}

    employee_dic3 = {'ope': 0.900000000000003, 'con': 0.633414931260427, 'ext': 0.8117213140033163, 'agr': 0.676611520481196, 'emo': 0.90000000000}

    #ibm_its = calc_similarity(target_dic, employee_dic1)
    #ibm_consuluting = calc_similarity(target_dic, employee_dic2)
    #ibm_designer = calc_similarity(target_dic, employee_dic3)

    get_recommended_companies(target_dic)
