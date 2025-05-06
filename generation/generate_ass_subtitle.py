def sec_to_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"  # ← .2fでピリオド

def auto_linebreak(text, max_len=10):
    # 10文字ごとに自動改行（\N）を挿入
    lines = []
    while len(text) > max_len:
        lines.append(text[:max_len])
        text = text[max_len:]
    lines.append(text)
    return r'\N'.join(lines)

def create_ass_file(subs, timestamps, ass_path, font="メイリオ"):
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(f"""[Script Info]
                ScriptType: v4.00+
                PlayResX: 1080
                PlayResY: 1920

                [V4+ Styles]
                Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
                Style: Default,{font},90,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,0,5,30,30,30,1

                [Events]
                Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
                """)
        for key, text in subs:
            start, end = timestamps[key]
            # 10文字ごとに自動改行
            text = auto_linebreak(text, max_len=10)
            f.write(f"Dialogue: 0,{sec_to_ass_time(start)},{sec_to_ass_time(end)},Default,,0,0,0,,{text}\n")