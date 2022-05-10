from pygame import mixer
from pathlib import Path
import time

from src.setting import get_settings, GlobalVariable
from src.api import download_audio, translate_text
from src.audio import play_audio, stop_audio

if __name__ == '__main__':
    g = GlobalVariable()

    # g.stop_playing

    # translate
    text = "The arguments shown above are merely the most common ones, described below in Frequently Used Arguments (hence the use of keyword-only notation in the abbreviated signature). The full function signature is largely the same as that of the Popen constructor - most of the arguments to this function are passed through to that interface. (timeout, input, check, and capture_output are not.)"
    result = translate_text(text)
    print(result)

    # play audio
    mixer.init()
    download_audio(text)
    # audio_path = Path(get_settings().TMP_DIR, "temp.mp3")
    # play_audio(g, mixer.music, audio_path)

    while mixer.music.get_busy():
        time.sleep(0.1)
