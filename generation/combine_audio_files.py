from pydub import AudioSegment
import os,re

def natural_sort_key(s):
    # 数字を抽出して、リストに分けて返す
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def combine_audio_with_silence(audio_folder, output_file, audio_format):
    # もし出力ファイル(final_output.mp3)が既に存在していたら削除
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"既存の出力ファイルを削除しました: {output_file}")

    silence_duration_ms = 500

    silence = AudioSegment.silent(duration=silence_duration_ms)
    combined = AudioSegment.empty()
    timestamps = []
    current_time = 0

    files = sorted(os.listdir(audio_folder), key=natural_sort_key)
    for filename in files:
        #print(f"filename={filename}")
        if filename.endswith(audio_format) and filename != os.path.basename(output_file):
            file_path = os.path.join(audio_folder, filename)
            audio = AudioSegment.from_mp3(file_path)

            timestamps.append(current_time / 1000)
            combined += audio
            combined += silence

            current_time += len(audio) + silence_duration_ms

    combined.export(output_file, format="mp3")
    print(f"結合完了！: {output_file}")

    # 結合後、元ファイルを全部削除
    for filename in files:
        if filename.endswith(audio_format) and filename != os.path.basename(output_file):
            os.remove(os.path.join(audio_folder, filename))
    print("元の音声ファイルを削除しました")

    print(f"各コメントの開始タイムスタンプ: {timestamps}")
    return timestamps
