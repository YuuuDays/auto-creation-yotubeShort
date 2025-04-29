import subprocess
import time
import requests
import os
from dotenv import load_dotenv


# 1. VOICEVOXエンジンを起動する
def start_voicevox_engine():

    load_dotenv()
    url = os.environ['VOICEVOX_PATH']
    engine_path = url
    subprocess.Popen([engine_path])
    print("VOICEVOXエンジン起動中...")
    time.sleep(5)  # 起動にちょっと時間かかるので少し待つ（調整可）


# コメントリストと話者リストから音声を作る
def generate_all_voices(comment_data):
    os.makedirs("output_audio", exist_ok=True)

    # 使いたいキャラクターのspeaker_id（例）
    speakers = [
        8,  # 青山龍星（イケボ）
        11,  # 玄野武宏（自然な低め）
        14,  # 白上虎太郎（元気め少年）
        17, #冥鳴ひまり（めいなきひまり
    ]

    for idx, (comment_id, text) in enumerate(comment_data):
        speaker_id = speakers[idx % len(speakers)]  # コメントごとに話者をローテーション
        output_path = os.path.join("output_audio", f"voice_{comment_id}.wav")
        create_voice(text, speaker_id, output_path)


# テキストから音声ファイルを作成する関数
def create_voice(text, speaker_id, output_path):
    # クエリ作成
    query_payload = {
        "text": text,
        "speaker": speaker_id
    }
    query = requests.post("http://127.0.0.1:50021/audio_query", params=query_payload)
    query.raise_for_status()

    # 音声合成
    synthesis_payload = {
        "speaker": speaker_id
    }
    synthesis = requests.post("http://127.0.0.1:50021/synthesis", params=synthesis_payload, data=query.text)
    synthesis.raise_for_status()

    # ファイル保存
    with open(output_path, "wb") as f:
        f.write(synthesis.content)

    print(f"保存完了！: {output_path}")

    # ピー音加工する
    #apply_beep_filter(output_path, text)



# 音声クエリを取得するだけの関数（再利用用）
def get_audio_query(text, speaker_id):
    response = requests.post(
        "http://127.0.0.1:50021/audio_query",
        params={"text": text, "speaker": speaker_id}
    )
    response.raise_for_status()
    return response.json()


def estimate_word_timings(audio_query_json):
    total_duration = 0.0
    for accent_phrase in audio_query_json['accent_phrases']:
        for mora in accent_phrase['moras']:
            total_duration += mora['consonant_length'] if mora.get('consonant_length') else 0
            total_duration += mora['vowel_length']

    timings = []
    current_time = 0.0
    for accent_phrase in audio_query_json['accent_phrases']:
        for mora in accent_phrase['moras']:
            start_time = current_time
            duration = 0
            if mora.get('consonant_length'):
                duration += mora['consonant_length']
            duration += mora['vowel_length']
            end_time = start_time + duration
            timings.append((mora['text'], start_time, end_time))
            current_time = end_time

    return timings
