import os
import subprocess
from PIL import ImageFont

def escape_text_for_ffmpeg(text):
    # 必要最低限のエスケープだけ
    return text.replace('\\', '\\\\').replace(':', '\\:').replace("'", "\\'").replace('"', '\\"')


def generate_video_with_subtitles(timestamps, text_dict, audio_path, tmp_background_video_path, output_path="final_output_with_subs.mp4"):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        for file in os.listdir(output_dir):
            if file.endswith(".mp4"):
                os.remove(os.path.join(output_dir, file))

    total_duration = timestamps[-1][1]
    font_path = os.path.abspath("assets/fonts/irohamaru-Medium.ttf").replace("\\", "/")
    print(f"[DEBUG] font_path: {font_path}")
    if not os.path.exists(font_path):
        print("[ERROR] フォントファイルが見つかりません！")
    else:
        print("[OK] フォントファイルは存在します。")
    font = ImageFont.truetype(font_path, size=40)

    # drawtext フィルタの生成
    drawtext_filters = []
    for i, (key, text) in enumerate(text_dict):
        start_time, end_time = timestamps[i]
        safe_text = escape_text_for_ffmpeg(text)

        filter_str = (
            f'drawtext=fontfile={font_path}:text="{safe_text}":'
            f'fontsize=80:fontcolor=white:box=1:boxcolor=black@0.5:alpha=1:'
            f'x=(w-text_w)/2:y=(h-text_h)/2:enable=\'between(t,{start_time},{end_time})\''
        )
        drawtext_filters.append(filter_str)

    full_filter = ",".join(drawtext_filters)

    cmd = [
        "ffmpeg",
        "-stream_loop", "-1",
        "-i", tmp_background_video_path,
        "-i", audio_path,
        "-vf", full_filter,
        "-t", str(total_duration),
        "-r", "30",
        "-c:v", "libx264",
        "-preset", "medium",  # エンコード品質の設定
        "-crf", "23",        # 品質設定（18-28の範囲、低いほど高品質）
        "-c:a", "aac",
        "-b:a", "192k",
        "-y",  # 上書き許可
        output_path
    ]

    print(f"[DEBUG] ffmpegコマンド: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("[ERROR] ffmpeg実行時にエラーが発生しました")
        print(e)
    else:
        print(f"✅ 動画生成完了: {output_path}")
