from gtts import gTTS
import os

"""
概要:テキストファイルから音声を作成
"""

def generate_audio(comment_data) -> None:
    # タプルinリストを一つのリストへ
    value_list = [value for key, value in comment_data]
    #print(value_list)
    # リストを1つの文章にまとめる
    text = "\n".join(value_list)
    print(text)

    try:
        # 保存先フォルダ
        output_dir = "OUTPUT"
        # フォルダがなかったら作る
        os.makedirs(output_dir, exist_ok=True)
        # ファイルパス作成
        output_path = os.path.join(output_dir, "output.mp3")

        tts = gTTS(text=text, lang='ja')
        tts.save(output_path)
        print("音声ファイルを保存しました")
    except Exception as e:
        print("エラーが発生しました:", e)



