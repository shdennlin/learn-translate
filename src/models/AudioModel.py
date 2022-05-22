from loguru import logger
from pathlib import Path
from pygame import mixer

from .setting import GlobalVariable

class AudioModel():

    @logger.catch
    def play_audio(g: GlobalVariable, audio: mixer.music, audio_path: Path):
        audio.load(audio_path)
        audio.play()
        logger.debug("play sound ({})".format(audio_path))


    @logger.catch
    def stop_audio(audio: mixer.music, audio_path: Path):
        audio.stop()
        logger.debug("stop sound ({})".format(audio_path))
