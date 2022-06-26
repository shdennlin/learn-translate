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


def test_query_vocabulary():
    assert model.query_vocabulary() is 200


def test_query_sentence():
    model.text = "I am a handsome boy"
    assert model.query_sentence() is 200
