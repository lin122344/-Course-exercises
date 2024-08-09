import os
from openai import OpenAI


#利用openAI類別
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
   ) 

#完成一個對話
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "我喜歡吃蘋果。",
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)