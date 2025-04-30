# generation/generate_video_with_subtitles.py
import os
import subprocess
from PIL import ImageFont


def generate_video_with_subtitles(timestamps, text_dict, audio_path, output_path="final_output_with_subs.mp4"):
    # 出力先フォルダを確認し、既存の.mp4ファイルを削除
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        for file in os.listdir(output_dir):
            if file.endswith(".mp4"):
                file_path = os.path.join(output_dir, file)
                os.remove(file_path)
                print(f"🗑️ 既存の動画を削除しました: {file_path}")

    # 黒背景映像を生成（音声と同じ長さにする）
    duration = timestamps[-1][1]  # 最後のコメントの終了時刻
    width, height = 1080, 1920  # YouTube Shorts 向け縦動画

    # drawtextのコマンドを生成
    drawtext_filters = []

    # assets/fontsフォルダ直下にある"ttf"を指定
    font_path = "assets/fonts/irohamaru-Medium.ttf"
    font = ImageFont.truetype(font_path, size=40)


    for i, (key, text) in enumerate(text_dict):
        start_time, end_time = timestamps[i]
        filter_str = (
            f"drawtext=fontfile={font_path}:text='{text}':"
            f"fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5:"
            f"x=(w-text_w)/2:y=h-200:enable='between(t,{start_time},{end_time})'"
        )
        drawtext_filters.append(filter_str)

    full_filter = ",".join(drawtext_filters)

    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", f"color=c=black:s={width}x{height}:d={duration}",
        "-i", audio_path,
        "-vf", full_filter,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ 動画生成完了: {output_path}")
