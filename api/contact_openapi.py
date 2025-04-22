import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

"""
    youtubeのタイトルを考える
"""
def convert_title_to_slang(title):
    prompt = f"""
元のタイトル: 「{title}」
これをほんの少しアレンジしてなんJスレタイ風に書き換えてください。ネットスラングや煽りっぽい言い回しを使い、スレタイっぽく短くユーモラスにしてください。
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    return response.choices[0].message.content.strip()

