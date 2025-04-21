# utils.py
def save_output_to_file(lines, filepath="output.txt"):
    """
    指定された行（リスト or 文字列）をファイルに保存する
    """
    with open(filepath, "w", encoding="utf-8") as f:
        if isinstance(lines, list):
            for line in lines:
                f.write(str(line) + "\n")
        else:
            f.write(str(lines))
