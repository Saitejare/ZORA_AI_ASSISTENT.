from pathlib import Path

import sounddevice as sd
import soundfile as sf


import sounddevice as sd


class AudioPlayer:

    def play(self, audio, sample_rate):

        sd.play(audio, sample_rate)

        sd.wait()