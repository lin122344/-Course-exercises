from openai import OpenAI
import os

def chat_with_chatgpt(user_message,openai_api_key):


    #利用openAI類別
    client = OpenAI(
        # This is the default and can be omitted
        api_key=openai_api_key) 

    #完成一個對話
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_message +'  請用有感情的方式回答一句話就好 。'
            }
        ],
        model="gpt-3.5-turbo",
    )

    response = chat_completion.choices[0].message.content
    return  response if response else "NO Content"


if __name__ == '__main__':

    user_message="我愛吃蘋果，你說你愛不愛"
    api_key=os.getenv("openAI_APIKEY",None)
    if api_key and user_message:
        response = chat_with_chatgpt(user_message,api_key)
        print(response)
    else:
        print("api key not found:",api_key)