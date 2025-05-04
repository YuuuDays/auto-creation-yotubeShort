# -*- coding: utf-8 -*-
# インポート文
import os
import threading
import subprocess

from generation.generate_video_with_subtitles import generate_video_with_subtitles
from generation.random_video_creator import concatenate_random_videos
from utils.logger import get_logger

# 自作モジュール
from generation.audio_creation_voicevox import start_voicevox_engine, generate_all_voices
from scraping.fetch_threads import scraping_website
from content_processing.fillter import filter_mask_text
from api.contact_openapi import convert_title_to_slang
from content_processing.extract_text_and_image import extract_images_and_texts
from generation.p_voice_filter import apply_beep_filter_from_text
from generation.combine_audio_files import combine_audio_with_silence
from generation.generate_ass_subtitle import create_ass_file


# グローバル定数
audio_format = ".wav"

# ロガー
logger = get_logger(__name__)


# ================================
# メイン処理
# ================================
def main():
    print("--処理開始--")

    """""""""""""""""""""
    対象のサイトからスクレイピング
    """""""""""""""""""""
    output_object = scraping_website()
    logger.info(f"[DBG]元のtitle ={output_object[0]}")
    # logger.debug(f"[DBG]内容 ={output_object[1]}")    #str

    """""""""""""""""""""
    OpenAPIにタイトルを考えさせる
    """""""""""""""""""""
    title_to_slang = convert_title_to_slang(output_object[0])
    logger.info(f"OpenAPIが考えたtitle ={title_to_slang}")

    """""""""""""""""""""
    タイトルに使われる不適切な文字の伏字処理
    """""""""""""""""""""
    # タイトルのマスク作業
    filtered_titles = filter_mask_text(title_to_slang)
    logger.info(f"OpenAPIが考えたtitleフィルター済み ={filtered_titles}")

    # 内容の加工(不要なスタイル指定や文字を削除)
    image_dict, text_dict = extract_images_and_texts(output_object[1])
    # for i in image_dict:
    #     print(image_dict[i])
    # for j in text_dict:
    #     print(j)

    # """""""""""""""""""""""""""
    # VOICEの作成
    # """""""""""""""""""""""""""
    start_voicevox_engine()
    # voiceの作成
    generate_all_voices(text_dict)

    # =================================
    # ピー音加工 & テキスト伏字処理
    # =================================
    # 加工済みコメント
    edited_comment = []

    for key, original_text in text_dict:
        #　伏字処理
        masked_text = filter_mask_text(original_text)
        edited_comment.append((key,masked_text))    # [(コメントの添え字, 伏字加工済みのコメント),(...,...)]

        # ピー音処理済みファイルの上書き
        wav_path = f"output_audio/voice_{key}.wav"
        apply_beep_filter_from_text(wav_path, original_text, masked_text)


    # output_audioフォルダの中にある音声ファイルを一つの音声ファイルに結合
    timestamps = combine_audio_with_silence("output_audio", "output_audio/final_output.mp3",audio_format)

    """
    タイムスタンプを元にランダム背景動画を作成
    """
    tmp_background_video_path = "temp/background_ready.mp4"
    concatenate_random_videos(tmp_background_video_path, timestamps)

    """""""""""""""""""""
    動画に字幕を焼き込む
    """""""""""""""""""""
    # === ASS字幕ファイルを作成 ===
    ass_path = "subtitle.ass"
    create_ass_file(edited_comment, timestamps, ass_path, "メイリオ")

    # === ffmpegでASS字幕を焼き込む ===
    output_video_path = "output_movie/final_output_with_subs.mp4"
    cmd = [
    "ffmpeg",
    "-i", tmp_background_video_path,
    "-i", "output_audio/final_output.mp3",
    "-vf", f"ass={ass_path}",
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-t", str(timestamps[-1][1]),
    "-r", "30",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "23",
    "-c:a", "aac",
    "-b:a", "192k",
    "-y",
    output_video_path
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ 動画生成完了: {output_video_path}")

    # ここでインド人を右へ

# メイン処理
if __name__ == "__main__":
    main()