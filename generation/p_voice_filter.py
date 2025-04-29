from pydub import AudioSegment
from pydub.generators import Sine
from content_processing.fillter import ng_words  # NGワード辞書
from generation.audio_creation_voicevox import get_audio_query, estimate_word_timings

def apply_beep_filter_from_text(wav_path, original_text, masked_text, speaker_id=1):
    print(f"ピー音加工対象: {wav_path}")

    if original_text == masked_text:
        print("NGワードなし、ピー音不要")
        return

    audio = AudioSegment.from_wav(wav_path)
    query_json = get_audio_query(original_text, speaker_id)
    timings = estimate_word_timings(query_json)

    # ピー音設定
    beep_volume = -19
    beep_freq = 1000
    beep_margin_ms = 100

    # 伏字の位置を確認
    new_audio = audio
    offset = 0
    found = False

    for i, (orig_char, mask_char) in enumerate(zip(original_text, masked_text)):
        if orig_char != mask_char:
            # moraのindexに変換（単純にiを使うとズレることもあるが、ここでは簡易的に）
            try:
                start_time = timings[i][1] * 1000 - beep_margin_ms
                end_time = timings[i][2] * 1000 + beep_margin_ms
                start_time = max(0, int(start_time))
                end_time = min(len(audio), int(end_time))

                beep = Sine(beep_freq).to_audio_segment(duration=end_time - start_time) + beep_volume
                new_audio = new_audio[:start_time] + beep + new_audio[end_time:]
                found = True
                print(f"ピー音挿入: {original_text[i]} [{start_time}ms - {end_time}ms]")
            except IndexError:
                print(f"タイミング推定失敗: {original_text[i]}")

    if found:
        new_audio.export(wav_path, format="wav")
        print(f"保存完了（ピー音追加済）: {wav_path}")
