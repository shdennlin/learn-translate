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

    @logger.catch
    def _download_audio(self,
                        languageCode="en-US",
                        audio_path=Path(get_settings().TMP_DIR, "temp.mp3")):
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
        return:
        1. 200 -> requests.get(post)
        2. 404 -> ""
        3. else-> None
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
        return:
        1. 200 -> requests.get(post)
        2. 404 -> ""
        3. else-> None
        """
        word = self.text
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        response = requests_funs("Free Dictionary API", "get", url)
        return response

    @logger.catch
    def _google_dict_api(self,
                         source_lanuage="auto",
                         target_language="zh_TW",
                         ui_language="en"):
        """
        return:
        1. 200 -> requests.get(post)
        2. 404 -> ""
        3. else-> None
        """
        word = self.text
        url = "https://translate.googleapis.com/translate_a/single"

        params = {
            "client": "gtx",
            "ie": "UTF-8",
            "oe": "UTF-8",
            "dt": ["bd", "ex", "ld", "md", "rw", "rm", "ss", "t", "at", "qc"],
            "sl": source_lanuage,
            "tl": target_language,
            "hl": ui_language,
            "q": word
        }

        response = requests_funs("Google free Dictionary API", "get", url,
                                 params)
        return response

    @logger.catch
    def _ecdict_query_api(self):
        word = self.text
        return self.ecdict_api.query(word)

    @logger.catch
    def query_vocabulary(self):
        word = self.text
        # correct word error
        word = Word(word).correct()
        self.text = word

        res = dict()
        res["word"] = word

        ecdict_data = self._ecdict_query_api()
        google_dict_api_ch_response = self._google_dict_api()
        google_dict_api_ch_data = google_dict_api_ch_response.json()

        res["translation"] = google_dict_api_ch_data[0][0][0]
        if ecdict_data != None:
            res["phonetic"] = ecdict_data["phonetic"]
            res["exchange"] = ecdict_data["exchange"]

            num_of_pos = len(google_dict_api_ch_data[1])
            res["pos"] = dict()

            for i in range(num_of_pos):
                res["pos"][google_dict_api_ch_data[1][i][0]] = dict()
                res["pos"][google_dict_api_ch_data[1][i][0]
                           ]["mean_zh"] = google_dict_api_ch_data[1][i][1]
                res["pos"][google_dict_api_ch_data[1][i][0]
                           ]["mean_en"] = google_dict_api_ch_data[12][i][1][0][0]
                res["pos"][google_dict_api_ch_data[1][i][0]
                           ]["sentences"] = google_dict_api_ch_data[12][i][1][0][2]

        if res != {}:
            self.res = res
            return 200
        else:
            return 404

    @logger.catch
    def query_sentence(self):
        text = self.text

        res = None
        google_dict_api_ch_response = self._google_dict_api()
        google_dict_api_ch_data = google_dict_api_ch_response.json()
        if google_dict_api_ch_data != "" or None:
            res = google_dict_api_ch_data[0][0][0]
            self.res = res

        if res != None:
            return 200
        else:
            return 404
