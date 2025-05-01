import os

# 概要:前に削除するファイルを削除する
def delete_previous_file( output_file:str ):
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"既存の出力ファイルを削除しました: {output_file}")