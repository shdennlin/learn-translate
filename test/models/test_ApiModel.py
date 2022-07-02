import pprint
import sys
from pathlib import Path

from src.models.ApiModel import ApiModel


model = ApiModel()
model.text = "strike"


def test_download_audio():
    assert model._download_audio() is not None


def test_google_translate_api():
    assert model._google_translate_api() is not None


def test_free_dict_api():
    assert model._free_dict_api() is not None


def test_google_dict_api():
    assert model._google_dict_api() is not None


def test_get_text_translate():
    assert model._get_text_translate("onshore") is 100 or 101
    assert model.res is not {}


def test_query():
    model.query("strike")
    assert model.res_html_en is not ""
    assert model.res_html_zh is not ""
