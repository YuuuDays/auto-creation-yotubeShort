import os
import random
import subprocess
from utils.delete_previous_file import delete_previous_file


def get_video_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def get_total_audio_duration(timestamps):
    return max(end for (_, end) in timestamps)


def concatenate_random_videos(output_path, timestamps, video_dir="assets/video_sources"):
    delete_previous_file(output_path)
    target_duration = get_total_audio_duration(timestamps)

    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(".mp4")]
    if not video_files:
        raise Exception("動画素材が見つかりません")

    selected_clips = []
    total_duration = 0
    last_clip = None

    while total_duration < target_duration:
        available_clips = [clip for clip in video_files if clip != last_clip and clip not in selected_clips]
        if not available_clips:
            raise Exception("使用できる動画が不足しています。")

        clip = random.choice(available_clips)
        duration_left = target_duration - total_duration
        clip_cut_duration = min(get_video_duration(clip), 7, duration_left)

        selected_clips.append((clip, clip_cut_duration))
        total_duration += clip_cut_duration
        last_clip = clip

    # トリミング済み一時ファイルを作成
    temp_clips = []
    for i, (clip, cut_duration) in enumerate(selected_clips):
        temp_output = f"temp_clip_{i}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-i", clip, "-t", str(cut_duration),
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-b:a", "128k", temp_output
        ], check=True)
        temp_clips.append(temp_output)

    # 結合リスト作成
    with open("temp_concat.txt", "w", encoding="utf-8") as f:
        for clip in temp_clips:
            f.write(f"file '{os.path.abspath(clip)}'\n")

    # 連結
    subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "temp_concat.txt",
    "-c:v", "libx264", "-preset", "ultrafast",
    "-c:a", "aac", "-b:a", "128k",
    output_path
], check=True)

    # クリーンアップ
    for clip in temp_clips:
        os.remove(clip)
    os.remove("temp_concat.txt")

    print(f"🎞 ランダム動画結合完了: {output_path}（音声長さにぴったり: {target_duration:.2f}秒）")
