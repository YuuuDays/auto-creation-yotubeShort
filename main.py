# -*- coding: utf-8 -*-
# インポート文
from generation.audio_creation import generate_audio
from generation.audio_creation_voicevox import start_voicevox_engine, generate_all_voices
from generation.combine_audio_files import combine_audio_with_silence
from scraping.fetch_threads import scraping_website
from content_processing.fillter import filter_mask_text
from utils.logger import get_logger
from api.contact_openapi import convert_title_to_slang
from content_processing.extract_text_and_image import extract_images_and_texts
# グローバル定数
audio_format = ".wav"

# 関数の定義
logger = get_logger(__name__)

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

    #generate_audio(text_dict)

    """""""""""""""""""""""""""
    VOICEの作成
    """""""""""""""""""""""""""
    # VICEVOXの初期化(起動)
    start_voicevox_engine()
    # voiceの作成
    generate_all_voices(text_dict)

    # output_audioフォルダの中にある音声ファイルを一つの音声ファイルに結合
    timestamps = combine_audio_with_silence("output_audio", "output_audio/final_output.mp3",audio_format)


# メイン処理
if __name__ == "__main__":
    main()