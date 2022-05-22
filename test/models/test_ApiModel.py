import unittest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.models.ApiModel import ApiModel


class TestApiModel(unittest.TestCase):

    def test__download_audio(self):
        model = ApiModel()
        model.text = "onshore"
        self.assertNotEqual(None, model._translate_text_api())

    def test_download_audio(self):
        model = ApiModel()
        model.text = "onshore"
        self.assertNotEqual(None, model._translate_text_api())

    def test_eng_eng_dict_api(self):
        model = ApiModel()
        model.text = "onshore"
        self.assertNotEqual(None, model._eng_eng_dict_api())

    def test_google_dict_api(self):
        model = ApiModel()
        model.text = "onshore"
        self.assertNotEqual(None, model._google_dict_api())


if __name__ == '__main__':
    unittest.main()
