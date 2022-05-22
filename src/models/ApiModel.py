import base64
import os
from loguru import logger
from pathlib import Path

from ..usecases.usecases import requests_funs
from ..usecases.setting import get_settings


class ApiModel():

    @logger.catch
    def download_audio(text="",
                       languageCode="en-US",
                       audio_path=Path(get_settings().TMP_DIR, "temp.mp3")):
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
                fp.write(base64.b64decode(response["audioContent"]))

    @logger.catch
    def translate_text_api(word="", target="zh_TW"):
        """ return response.json()"""

        key = get_settings().TRANSLATION_API_KEY
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {"key": key, "target": target, "q": word}

        response = requests_funs("Cloud Translate API", "post", url, params)

        return response

    @logger.catch
    def eng_eng_dict_api(word=""):
        """ return response.json()"""

        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        response = requests_funs("Free Dictionary API", "get", url)
        return response

    @logger.catch
    def google_dict_api(word="test",
                        source_lanuage="auto",
                        target_language="zh_TW",
                        ui_language="en"):
        """ return response.json()"""

        url = "https://translate.googleapis.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&dt=bd&dt=ex&dt=ld&dt=md&dt=rw&dt=rm&dt=ss&dt=t&dt=at&dt=qc"

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
