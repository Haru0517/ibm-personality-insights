from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from utils import write_to_json


def analyze_personality():
    """個人のテキストをクエリとし，PersonalityInsightsから性格パラメータを取得する．

    Returns:
        dict: Big 5のパラメータ． keyは{'ope', 'con', 'ext', 'agr', 'emo'}
    """
    with open('apikey.txt', 'r') as f:
        api_key = f.read()

    authenticator = IAMAuthenticator(api_key)
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
