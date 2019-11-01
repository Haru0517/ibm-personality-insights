from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from utils import write_to_json


"""
curl -X POST -u “apikey:FOlbZkEEdYCkScLMUtNoRLb86B6zWP0saMeEBMA-vIv9” --header “Content-Type: text/plain;charset=utf-8" --header “Accept: application/json” --data-binary @Desktop/profile.txt --output profile.json  “https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13”
"""


def analyze_personality():
    """個人のテキストをクエリとし，PersonalityInsightsから性格パラメータを取得する．

    Returns:
        dict: Big 5のパラメータ． keyは{'ope', 'con', 'ext', 'agr', 'emo'}
    """
    authenticator = IAMAuthenticator('4VRR3O-EJCsh2cl1GDzcFo77bI0wo9A9P_1apIuse6hw')
    personality_insights = PersonalityInsightsV3(
        version='2017-10-13',
        authenticator=authenticator
    )

    personality_insights.set_service_url('https://gateway.watsonplatform.net/personality-insights/api')

    with open('sample.txt', 'r') as profile_text:
        profile = personality_insights.profile(
            profile_text.read(),
            'application/json',
            consumption_preferences=True,
            content_language='ja',
            accept_language='ja',
        ).get_result()

    json_obj = profile
    write_to_json(json_obj, 'json/result.json')

    ope = json_obj["personality"][0]["percentile"]
    con = json_obj["personality"][1]["percentile"]
    ext = json_obj["personality"][2]["percentile"]
    agr = json_obj["personality"][3]["percentile"]
    emo = json_obj["personality"][4]["percentile"]

    dic = {'ope': ope, 'con': con, 'ext': ext, 'agr': agr, 'emo': emo}

    return dic


if __name__ == '__main__':
    a = analyze_personality()
    print(a)
