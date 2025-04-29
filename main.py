# -*- coding: utf-8 -*-
# インポート文
import os
import threading
from utils.logger import get_logger

# 自作モジュール
from generation.audio_creation_voicevox import start_voicevox_engine, generate_all_voices
from scraping.fetch_threads import scraping_website
from content_processing.fillter import filter_mask_text
from api.contact_openapi import convert_title_to_slang
from content_processing.extract_text_and_image import extract_images_and_texts
from generation.p_voice_filter import apply_beep_filter_from_text
from generation.combine_audio_files import combine_audio_with_silence


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
    # ピー音加工
    # =================================
    for key, original_text in text_dict:
        masked_text = filter_mask_text(original_text)
        wav_path = f"output_audio/voice_{key}.wav"
        apply_beep_filter_from_text(wav_path, original_text, masked_text)

    # output_audioフォルダの中にある音声ファイルを一つの音声ファイルに結合
    timestamps = combine_audio_with_silence("output_audio", "output_audio/final_output.mp3",audio_format)


# メイン処理
if __name__ == "__main__":
    main()