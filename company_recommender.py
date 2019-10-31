import json


def calc_similarity(target_dic, employee_dic):

    keys = list(target_dic.keys())

    ibm_profession = 0
    for key in keys:
        ibm_profession =+ (abs(target_dic[key]-employee_dic[key]))

    precision_profession = (1/(1+ibm_profession))*100

    return precision_profession


def get_company_list(target_dic):
    """類似度が高い順にソートして返す"""



    return


if __name__ == '__main__':
    target_dic = {'ope': 0.8243266441684023, 'con': 0.633414931260427, 'ext': 0.8117213140033163, 'agr': 0.676611520481196, 'emo': 0.5190227982392853}

    employee_dic1 = {'ope': 0.8143266441684023, 'con': 0.623414931260427, 'ext': 0.8017213140033163, 'agr': 0.66611520481196, 'emo': 0.5090227982392853}

    employee_dic2 = {'ope': 0.5555555555555555, 'con': 0.633414931260427, 'ext': 0.9999999999, 'agr': 0.99999999999, 'emo': 0.1111111111111}

    employee_dic3 = {'ope': 0.900000000000003, 'con': 0.633414931260427, 'ext': 0.8117213140033163, 'agr': 0.676611520481196, 'emo': 0.90000000000}

    ibm_its = calc_similarity(target_dic, employee_dic1)
    ibm_consuluting = calc_similarity(target_dic, employee_dic2)
    ibm_designer = calc_similarity(target_dic, employee_dic3)
