import requests
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json


"""
curl -X POST -u “apikey:FOlbZkEEdYCkScLMUtNoRLb86B6zWP0saMeEBMA-vIv9” --header “Content-Type: text/plain;charset=utf-8" --header “Accept: application/json” --data-binary @Desktop/profile.txt --output profile.json  “https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13”
"""

def analyze_personality():
    # APIインスタンスを生成
    authenticator = IAMAuthenticator('FOlbZkEEdYCkScLMUtNoRLb86B6zWP0saMeEBMA-vIv9')
    personality_insights = PersonalityInsightsV3(
        version='2017-10-13',
        authenticator=authenticator
    )
    personality_insights.set_service_url('https://gateway-tok.watsonplatform.net/personality-insights/api')

    personality_insights.set_detailed_response(True)
    response = personality_insights.methodName(parameters)
    # Access response from methodName
    print(json.dumps(response.get_result(), indent=2))
    # Access information in response headers
    print(response.get_headers())
    # Access HTTP response status
    print(response.get_status_code())

    exit()


    # 性格を分析
    with open('sample.txt', 'r') as profile_text:
        profile = service.profile(
            profile_text.read(),
            'application/json',
            content_language='ja',
            accept_language='ja').get_result()

    # ファイルに書き込み
    with open('result.json', 'w') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    analyze_personality()