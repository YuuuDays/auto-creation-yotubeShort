import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils.output_text import save_output_to_file
from utils.logger import get_logger

logger = get_logger(__name__)

def scraping_website()-> tuple[str,str]:
    logger.info("スレッドの取得開始")
    # .envファイルの内容を読み込見込む
    load_dotenv()

    url = os.environ['WEB_URL']
    #url = "https://www.python.org/"
    r   = requests.get(url)

    print(r.status_code) #200を期待
    if r.status_code != 200:
       raise Exception(f"ステータスコードが200ではありません: {r.status_code}")
    #r.raise_for_status()  # ←こっちでも200系以外ならHTTPErrorがraiseされる

    #print(r.text)

    print("------------------------------")
    soup = BeautifulSoup(r.content,'html.parser')

    # タイトル出力
    title = soup.title.string
    # タイトル| HP名の '|'から以下を削除
    molding_title = title.split("｜")[0].strip()
    logger.debug(f"[DNG]title is {molding_title}")

    # tagの確認
    # for tag in soup.find_all("div"):
    #     if "entrybody" in tag.get("class",[]):
    #         print(tag)
            #save_output_to_file(tag, "soup_output.txt")

    # 中身のHTML要素だけ（=タグの中の部分）を取得
    entry_div = soup.select_one("div.entrybody")
    #print(entry_div.decode_contents())

    # テキストに出力
    save_output_to_file(entry_div.decode_contents(), "soup_output.txt")

    # 特定の要素を取得


    return molding_title,entry_div.decode_contents()