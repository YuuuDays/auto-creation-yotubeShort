# -*- coding: utf-8 -*-
# インポート文
from scraping.fetch_threads import scraping_website


# グローバル定数

# 関数の定義
def main():
    print("--処理開始--")
    outputMSG = scraping_website()
    print(f"outputMSG ={outputMSG}")


# メイン処理
if __name__ == "__main__":
    main()