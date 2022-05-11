# -*- coding: utf-8 -*-
from pygame import mixer
from pathlib import Path
import time

from src.setting import get_settings, GlobalVariable
from src.api import download_audio, translate_text_api, english_dict_api
from src.audio import play_audio, stop_audio
import src.stardict as startdict

if __name__ == '__main__':
    g = GlobalVariable()

    stardict_db_path = Path(get_settings().BASE_DIR, "data", "stardict.db")
    engdict = startdict.StarDict(stardict_db_path)
    # res_match = engdict.match("gather up")
    # res = engdict.query(res_match[0][1])

    #==================================================================
    # English Dict
    text = "arguments"
    result = english_dict_api(text)
    print(result)

    #==================================================================
    # Query
    # text = "ASAP"
    # res = engdict.query(text)
    # if res == None:
    #     res = translate_text_api(text)

    # print(res)

    #==================================================================
    # translate
    # text = "The arguments shown above are merely"
    # result = translate_text_api(res["translation"])
    # print(result)

    #==================================================================
    # play audio
    # mixer.init()
    # download_audio(text)
    # audio_path = Path(get_settings().TMP_DIR, "temp.mp3")
    # play_audio(g, mixer.music, audio_path)

    # while mixer.music.get_busy():
    #     time.sleep(0.1)
