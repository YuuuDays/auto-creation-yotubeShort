import random
from generation.audio_creation_voicevox import get_audio_query, estimate_word_timings

def sec_to_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def auto_linebreak(text, max_len=8):
    lines = []
    while len(text) > max_len:
        lines.append(text[:max_len])
        text = text[max_len:]
    lines.append(text)
    return r'\N'.join(lines)

def random_color():
    # ASSの色はBGR順、&H00BBGGRR
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"&H00{b:02X}{g:02X}{r:02X}"

def colorize_text(text, color="&H00FF00&"):
    # 例：全体を色付きにしたい場合
    return r"{\c" + color + "}" + text + r"{\c&HFFFFFF&}"  # 最後で白に戻す

def create_ass_file(subs, timestamps, ass_path, font="メイリオ"):
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
""")
        # 各コメントごとにランダム色のStyleを作成
        for idx, (key, text) in enumerate(subs):
            color = random_color()
            # 余白を広めに（例：左右120px）
            f.write(f"Style: Karaoke{idx},{font},90,&H00FFFFFF,{color},&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,0,5,120,120,30,1\n")

        f.write("""
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
        for idx, (key, text) in enumerate(subs):
            start, end = timestamps[key]
            # VOICEVOXのタイミング取得
            query_json = get_audio_query(text, 8)  # speaker_idは適宜
            timings = estimate_word_timings(query_json)
            # カラオケタグ生成
            karaoke_line = ""
            for i, (char, t) in enumerate(zip(text, timings)):
                duration_cs = int((t[2] - t[1]) * 100)  # 1/100秒単位
                karaoke_line += f"{{\\k{duration_cs}}}{char}"
            # 7～8文字ごとに改行
            karaoke_line = auto_linebreak(karaoke_line, max_len=8)
            # Dialogue出力（Styleをコメントごとに割り当て）
            f.write(f"Dialogue: 0,{sec_to_ass_time(start)},{sec_to_ass_time(end)},Karaoke{idx},,0,0,0,,{karaoke_line}\n")