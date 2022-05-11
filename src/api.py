import base64
import os
import requests
from loguru import logger
from pathlib import Path

from .setting import get_settings


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
def translate_text_api(text="", target="zh_TW"):

    key = get_settings().TRANSLATION_API_KEY
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {"key": key, "target": target, "q": text}

    response = requests.post(url, params=params)
    logger.debug(f"cloud translation response = {response.status_code}")
    if response.status_code == 200:
        response = response.json()["data"]["translations"][0]["translatedText"]
        logger.debug(f"cloud translation text = {response}")
        return response
    else:
        logger.error(
            f"cloud translation response error, status_code = {response.status_code}"
        )


@logger.catch
def english_dict_api(text=""):

    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + text

    response = requests.get(url)
    logger.debug(f"English Dictionary response = {response.status_code}")
    if response.status_code == 200:
        response = response.json()
        logger.debug(f"English Dictionary text = {response}")
        return response
    else:
        logger.error(
            f"cloud translation response error, status_code = {response.status_code}"
        )
