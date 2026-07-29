from pathlib import Path

import sounddevice as sd
import soundfile as sf


class AudioPlayer:

    def play(self, audio_path: Path):

        audio, sample_rate = sf.read(audio_path)

        sd.play(audio, sample_rate)

        sd.wait()