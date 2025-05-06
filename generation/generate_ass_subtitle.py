import random

def sec_to_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def auto_linebreak(text, max_len=10):
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

def create_ass_file(subs, timestamps, ass_path, font="メイリオ"):
    num_styles = len(subs)
    style_names = []
    style_defs = ""
    for i in range(num_styles):
        style_name = f"Style{i}"
        color = random_color()
        style_defs += f"Style: {style_name},{font},90,{color},&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,0,5,30,30,30,1\n"
        style_names.append(style_name)

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{style_defs}
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
        for idx, (key, text) in enumerate(subs):
            start, end = timestamps[key]
            text = auto_linebreak(text, max_len=10)
            style = style_names[idx]
            f.write(f"Dialogue: 0,{sec_to_ass_time(start)},{sec_to_ass_time(end)},{style},,0,0,0,,{text}\n")