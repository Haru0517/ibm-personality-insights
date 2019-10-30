
from ibm_watson import PersonalityInsightsV3
import json


"""
curl -X POST -u “apikey:FOlbZkEEdYCkScLMUtNoRLb86B6zWP0saMeEBMA-vIv9” --header “Content-Type: text/plain;charset=utf-8" --header “Accept: application/json” --data-binary @Desktop/profile.txt --output profile.json  “https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13”
"""


def analyze_personality():
    from ibm_watson import PersonalityInsightsV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from os.path import join, dirname
    import json

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
    print(json.dumps(profile, indent=2))


if __name__ == '__main__':
    analyze_personality()