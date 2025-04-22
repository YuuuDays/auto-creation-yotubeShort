# -*- coding: utf-8 -*-
# インポート文
from scraping.fetch_threads import scraping_website
from content_processing.fillter import filter_mask_text
from utils.logger import get_logger
from api.contact_openapi import convert_title_to_slang
from content_processing.extract_text_and_image import extract_images_and_texts
# グローバル定数

# 関数の定義
logger = get_logger(__name__)

def main():
    print("--処理開始--")

    """ 
    対象のサイトからスクレイピング
    """
    output_object = scraping_website()
    logger.info(f"成形前title ={output_object[0]}")
    logger.debug(f"[DBG]内容 ={output_object[1]}")    #str

    """
    OpenAPIにタイトルを考えさせる
    """
    title_to_slang = convert_title_to_slang(output_object[0])
    logger.info(f"OpenAPIが考えたtitle ={title_to_slang}")

    # タイトルのマスク作業
    filtered_titles = filter_mask_text(title_to_slang)
    logger.info(f"OpenAPIが考えたtitleフィルター済み ={filtered_titles}")

    # 内容の加工(不要なスタイル指定や文字を削除)
    extract_images_and_texts(output_object[1])




# メイン処理
if __name__ == "__main__":
    main()