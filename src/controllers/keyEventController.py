import threading
import time
from pynput.keyboard import Listener, Key

class keyEventListener():
    def __init__(self):
        pass

    @staticmethod
    def on_release(key):
        print("Release")
        print(key)  
        

    def run(self):
        print("Listen thread start!")
        listener = Listener(
            on_release=self.on_release
        )
        listener.start()
