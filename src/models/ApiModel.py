import base64
import os
from pprint import pprint
from pathlib import Path

from loguru import logger
from textblob import Word

from ..setting import get_settings
from ..usecases.stardict import StarDict
from ..usecases.usecases import requests_funs


class ApiModel():

    def __init__(self):
        self.text = ""
        self.ecdict_db_path = Path(get_settings().BASE_DIR, "data",
                                   "stardict.db")
        self.ecdict_api = StarDict(self.ecdict_db_path)
        self.res = ""
        self.res_html_en = ""
        self.res_html_zh = ""

    @logger.catch
    def _download_audio(self,
                        languageCode="en-US",
                        audio_path=Path(get_settings().TMP_DIR, "temp.mp3")):
        """
        Returns:
        resquests.post
        """
        text = self.text
        key = get_settings().TEXT_TO_SPEECH_API_KEY
        url = "https://texttospeech.googleapis.com/v1/text:synthesize"
        params = {"key": key}
        json = {
            "voice": {
                "languageCode": languageCode
            },
            "input": {
                "text": text
            },
            "audioConfig": {
                "audioEncoding": "mp3"
            }
        }

        response = requests_funs("Cloud Text to Speech API", "post", url,
                                 params, json)
        try:
            os.remove(audio_path)
        except:
            pass

        if response:
            with open(audio_path, 'wb') as fp:
                fp.write(base64.b64decode(response.json()["audioContent"]))

        return response

    @logger.catch
    def _google_translate_api(self, target="zh_TW"):
        """
        Returns:
        resquests.post
        """
        word = self.text
        key = get_settings().TRANSLATION_API_KEY
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {"key": key, "target": target, "q": word}

        response = requests_funs("Cloud Translate API", "post", url, params)

        return response

    @logger.catch
    def _free_dict_api(self):
        """
        Returns:
        resquests.get
        """
        word = self.text
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        response = requests_funs("Free Dictionary API", "get", url)
        return response

    @logger.catch
    def _google_dict_api(self,
                         source_language="auto",
                         target_language="zh_TW",
                         ui_language="en"):
        """
        Returns:
        resquests.get
        """
        word = self.text
        url = "https://translate.googleapis.com/translate_a/single"

        params = {
            "client": "gtx",
            "ie": "UTF-8",
            "oe": "UTF-8",
            "dt": ["bd", "ex", "ld", "md", "rw", "rm", "ss", "t", "at", "qc"],
            "sl": source_language,
            "tl": target_language,
            "hl": ui_language,
            "q": word
        }

        response = requests_funs("Google free Dictionary API", "get", url,
                                 params)
        return response

    @logger.catch
    def _ecdict_query_api(self):
        """
        Returns:
        StarDict.query
        """
        word = self.text
        return self.ecdict_api.query(word)

    @logger.catch
    def _get_text_translate(self) -> int:
        """ query vocabulary
        Returns:
            100: Vocabulary is found
            101: Sentence is found or Vocabulary is WRONG
        """
        # correct word error
        # text = self.text
        # if len(text.split()) == 1:
        #     text = Word(text).correct()
        # self.text = text

        res = dict()

        ecdict_data = self._ecdict_query_api()
        google_dict_api_ch_response = self._google_dict_api()
        google_dict_api_ch_data = google_dict_api_ch_response.json()

        res["word"] = self.text
        res["translation"] = google_dict_api_ch_data[0][0][0]
        if ecdict_data != None:
            res["phonetic"] = ecdict_data["phonetic"]
            res["exchange"] = ecdict_data["exchange"]

            if google_dict_api_ch_data[1] != None:
                num_of_pos = len(google_dict_api_ch_data[1])
                res["pos"] = dict()

                for i in range(num_of_pos-1, -1, -1):
                    res["pos"][google_dict_api_ch_data[1][i][0]] = dict()
                    res["pos"][google_dict_api_ch_data[1][i][0]
                               ]["mean_zh"] = google_dict_api_ch_data[1][i][1]
                    res["pos"][google_dict_api_ch_data[1][i][0]
                               ]["mean_en"] = google_dict_api_ch_data[12][i][1][0][0]
                    # judge if have sentences
                    if not len(google_dict_api_ch_data[12][i][1][0]) < 3:
                        res["pos"][google_dict_api_ch_data[1][i][0]
                                   ]["sentences"] = google_dict_api_ch_data[12][i][1][0][2]
        self.res = res

        if ecdict_data != None and google_dict_api_ch_data[1] != None:
            return 100
        else:
            return 101

    @logger.catch
    def _process_text_to_html(self, status_code):
        def gray_html(text):
            return '<span style="color:gray;">{}</span>'.format(text)

        def bold_html(text):
            return '<b>{}</b>'.format(text)
        res = self.res
        res_html_en = ""
        res_html_zh = ""

        res_html_zh += res["translation"]

        if status_code == 100:  # if vocabulary is found
            res_html_en += " " + res["word"] + "<br>"
            res_html_zh += " " + gray_html(res["word"]) + "<br>"

            res_html_en += gray_html("[" + res["phonetic"] + "]") + "<br>"
            res_html_zh += gray_html("[" + res["phonetic"] + "]") + "<br>"

            res_html_en += gray_html(res["exchange"]) + "<br><br>"
            res_html_zh += gray_html(res["exchange"]) + "<br><br>"

            for key in res["pos"]:
                res_html_en += bold_html(key) + "<br>"
                res_html_zh += bold_html(key) + "<br>"

                res_html_zh += ", ".join(i for i in res["pos"]
                                         [key]["mean_zh"]) + "<br>"

                res_html_en += res["pos"][key]["mean_en"] + "<br>"
                res_html_zh += res["pos"][key]["mean_en"] + "<br>"

                if "sentences" in res["pos"][key]:
                    res_html_en += gray_html(res["pos"]
                                             [key]["sentences"]) + "<br>"
                    res_html_zh += gray_html(res["pos"]
                                             [key]["sentences"]) + "<br>"

                res_html_en += "<br>"
                res_html_zh += "<br>"

        self.res_html_en = res_html_en
        self.res_html_zh = res_html_zh

    def query(self, text):
        self.text = text
        status_code = self._get_text_translate()
        self._process_text_to_html(status_code)
