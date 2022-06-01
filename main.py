# -*- coding: utf-8 -*-
from multiprocessing.spawn import import_main_path
from pygame import mixer
from pathlib import Path
import sys
import time
import codecs
import json
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt


from src.controllers.keyEventController import keyEventListener
from src.controllers.controllers import Controller
from src.views.views import mainWindows
from src.models.ApiModel import ApiModel
# from src.models.ApiModel import *
# from src.models.AudioModel import *
# from src.setting import get_settings, GlobalVariable
# from src.api import download_audio, translate_text_api, eng_eng_dict_api, google_dict_api
# from src.audio import play_audio, stop_audio
# from src.get_result import get_word_means
# from src.stardict import StarDict
# from src.usecases import print_response_json, write_response_json


def main():
    g = GlobalVariable()

    word = "inhabit"
    # get_word_means(word, eng_chi_dict_api)

    word = "inhabit"
    s = time.time()
    #=====ECDICT==========================================================
    stardict_db_path = Path(get_settings().BASE_DIR, "data", "stardict.db")
    eng_chi_dict_api = StarDict(stardict_db_path)
    # res_match = eng_chi_dict_api.match("gather up")
    # res = eng_chi_dict_api.query(res_match[0][1])
    res = eng_chi_dict_api.query(word)
    write_response_json(res, Path(get_settings().TMP_DIR, "ECEICT.json"))

    # =====Cloud Translate API============================================
    res = translate_text_api(["bitch", "process"])
    if res:
        print(res["data"]["translations"])

    # =====Free Dictionary API============================================
    res = eng_eng_dict_api(word)
    # print_response_json(res)
    write_response_json(res,
                        Path(get_settings().TMP_DIR, "FreeDictionaryAPI.json"))

    # =====Google Dictionary API==========================================
    res = google_dict_api(word)
    # print_response_json(res)
    write_response_json(
        res, Path(get_settings().TMP_DIR, "GoogleDictionaryAPI.json"))

    # =====play audio=====================================================
    mixer.init()
    download_audio(word)
    e = time.time()
    print(e - s)

    audio_path = Path(get_settings().TMP_DIR, "temp.mp3")
    play_audio(g, mixer.music, audio_path)

    while mixer.music.get_busy():
        time.sleep(0.1)


class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = ApiModel()
        self.main_view = mainWindows()
        self.main_controller = Controller(self.main_view, self.model)

        self.main_view.show()


if __name__ == '__main__':
    KeyEventListener = keyEventListener()
    KeyEventListener.run()
    app = App(sys.argv)
    sys.exit(app.exec_())