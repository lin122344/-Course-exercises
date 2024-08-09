import os,sys

def get_secret_and_token():
    channel_secret = os.getenv('LINEBOT_KEY', None)
    channel_access_token = os.getenv('LINEBOT_ACCESS_TOKEN', None)
    openai_api_key = os.getenv("openAI_APIKEY",None)
    if channel_secret is None:
        print('Specify LINEBOT_KEY as environment variable.')
        sys.exit(1)
    if channel_access_token is None:
        print('Specify LINEBOT_ACCESS_TOKEN as environment variable.')
        sys.exit(1)
    if openai_api_key is None:
        print('Specify openAI_APIKEY as environment variable.')
        sys.exit(1)

    return{
        'LINEBOT_KEY':channel_secret,
        'LINEBOT_ACCESS_TOKEN':channel_access_token,
        'openAI_APIKEY': openai_api_key
    }