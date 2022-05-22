from loguru import logger

from .api import download_audio, translate_text_api, eng_eng_dict_api, google_dict_api
from .stardict import StarDict


def get_word_means(word: str, eng_chi_dict_api: StarDict):
    # English Dict
    eng_eng_dict_res = eng_eng_dict_api(word)
    eng_chi_dict_res = eng_chi_dict_api.query(word)
    google_dict_res = google_dict_api(word)

    result = dict()
    result["word"] = word
    # result["word"] = word
