from pydub import AudioSegment
import os,re

def natural_sort_key(s):
    # 数字を抽出して、リストに分けて返す
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def combine_audio_with_silence(audio_folder, output_file, audio_format):
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"既存の出力ファイルを削除しました: {output_file}")

    silence_duration_ms = 500
    silence = AudioSegment.silent(duration=silence_duration_ms)
    combined = AudioSegment.empty()
    timestamps = []  # [(start, end)] の形式
    current_time = 0

    files = sorted(os.listdir(audio_folder), key=natural_sort_key)
    for filename in files:
        if filename.endswith(audio_format) and filename != os.path.basename(output_file):
            file_path = os.path.join(audio_folder, filename)
            audio = AudioSegment.from_mp3(file_path)

            start_time = current_time / 1000  # 秒に変換
            end_time = (current_time + len(audio)) / 1000
            timestamps.append((start_time, end_time))

            combined += audio
            combined += silence
            current_time += len(audio) + silence_duration_ms

    combined.export(output_file, format="mp3")
    print(f"結合完了！: {output_file}")

    for filename in files:
        if filename.endswith(audio_format) and filename != os.path.basename(output_file):
            os.remove(os.path.join(audio_folder, filename))
    print("元の音声ファイルを削除しました")

    print(f"各コメントの開始・終了タイムスタンプ: {timestamps}")
    return timestamps
