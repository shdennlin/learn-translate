import base64
import os
import requests
from loguru import logger
from pathlib import Path

from .setting import get_settings


@logger.catch
def download_audio(word="",
                   languageCode="en-US",
                   audio_path=Path(get_settings().TMP_DIR, "temp.mp3")):
    key = get_settings().TEXT_TO_SPEECH_API_KEY
    url = "https://texttospeech.googleapis.com/v1/word:synthesize"
    params = {"key": key}
    json = {
        "voice": {
            "languageCode": languageCode
        },
        "input": {
            "word": word
        },
        "audioConfig": {
            "audioEncoding": "mp3"
        }
    }
    response = requests.post(url, params=params, json=json)
    if response.status_code == 200:
        os.remove(audio_path)
        with open(audio_path, 'wb') as fp:
            fp.write(base64.b64decode(response.json()["audioContent"]))
    else:
        logger.error(
            f"cloud translation response error, status_code = {response.status_code}"
        )


@logger.catch
def translate_text_api(word="", target="zh_TW"):
    """ return response.json()"""

    key = get_settings().TRANSLATION_API_KEY
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {"key": key, "target": target, "q": word}

    response = requests.post(url, params=params)
    logger.debug(f"cloud translation response = {response.status_code}")
    if response.status_code == 200:
        response = response.json()["data"]["translations"][0]["translatedText"]
        logger.debug(f"cloud translation word = {response}")
        return response
    else:
        logger.error(
            f"cloud translation response error, status_code = {response.status_code}"
        )


@logger.catch
def eng_eng_dict_api(word=""):
    """ return response.json()"""

    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word

    response = requests.get(url)
    logger.debug(f"English Dictionary API = {response.status_code}")
    if response.status_code == 200:
        response = response.json()
        logger.debug(
            f"English Dictionary API, word={word}, response={response}")
        return response
    elif response.status_code == 404:
        return None
    else:
        logger.error(
            f"cloud translation response error, status_code = {response.status_code}"
        )


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

    response = requests.get(url, params=params)
    logger.debug(f"Google free Dict API = {response.status_code}")
    if response.status_code == 200:
        response = response.json()
        logger.debug(f"Google free Dict API, word={word}, response={response}")
        return response
    elif response.status_code == 404:
        return None
    else:
        logger.error(
            f"Google free Dict API response error, status_code = {response.status_code}"
        )
