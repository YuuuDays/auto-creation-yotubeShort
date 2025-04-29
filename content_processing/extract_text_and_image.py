import re

from bs4 import BeautifulSoup

from content_processing.fillter import filter_mask_text

"""
スクレイピングした画像を含むテキストの不要部分を抽出
@in ...↑の内容のstr
@out...抽出した画像とテキストの辞書
"""
def extract_images_and_texts(html: str):
    soup = BeautifulSoup(html, 'html.parser')

    # 画像URLをすべて取得
    img_tags = soup.find_all('img')
    image_dict = {
        i: img['src'] for i, img in enumerate(img_tags) #enumerate ->インデックスと値を同時に取得する
        if 'src' in img.attrs and not img['src'].startswith('data:image')
    }

    print("---★---")
    #print(image_dict)

    # テキスト（bタグ内）をすべて取得
    tmp_list  =[]
    idx = 0

    print("+*+*+**+*+*+*+*+*")
    for div in soup.find_all('div', id=lambda x: x and x.startswith('resid')):
        b_tag = div.find('b')
        #print(b_tag)
        if b_tag:
            text = b_tag.get_text(strip=True)
            if text:
                # トリミング処理('>>数字'の部分の切り取り)
                convert_text = re.sub(r'>>\d+[，,]?','>>',text)
                # マスキング処理(fillter.pyの文言に対して伏字を行う)
                convert_text_filtered= filter_mask_text(convert_text)
                tmp_list.append(convert_text_filtered)
                # print(convert_text)

    # 作成したリストをタプルinリストへ
    text_dict = [(i,s) for i, s in enumerate(tmp_list)] # ← [(0,'xxx'),(1,'yyy'),...] タプルinリスト

    return image_dict,text_dict