import queue
from pathlib import Path
from collections import deque
import numpy as np
import sounddevice as sd
import soundfile as sf

from .config import (
    AUDIO_FILE,
    CHANNELS,
    FRAME_DURATION_MS,
    SAMPLE_RATE,
    SILENCE_DURATION,
)
from .config import (
    AUDIO_FILE,
    CHANNELS,
    FRAME_DURATION_MS,
    PRE_SPEECH_DURATION,
    SAMPLE_RATE,
    SILENCE_DURATION,
)
from .vad import VoiceActivityDetector


class SpeechRecorder:
    def __init__(self) -> None:
        self.vad = VoiceActivityDetector()
        self.frame_size = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)
        self.audio_queue: queue.Queue[np.ndarray] = queue.Queue()

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())

    def record(self) -> Path:
        recorded_frames = []
        buffer_size = int(PRE_SPEECH_DURATION * 1000 / FRAME_DURATION_MS)
        pre_buffer = deque(maxlen=buffer_size)
        recording = False
        silence_frames = 0
        max_silence = int(SILENCE_DURATION * 1000 / FRAME_DURATION_MS)

        print("🎤 Waiting for speech...")

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=self.frame_size,
            callback=self._callback,
        ):
            while True:
                frame = self.audio_queue.get()
                pre_buffer.append(frame)

                speech = self.vad.is_speech(
                    frame.tobytes(),
                    SAMPLE_RATE,
                )

                if speech:
                    if not recording:
                          print("🎙 Recording...")
                          recording = True
                          recorded_frames.extend(pre_buffer)

                    silence_frames = 0
                    recorded_frames.append(frame)

                elif recording:
                    recorded_frames.append(frame)
                    silence_frames += 1

                    if silence_frames >= max_silence:
                        print("✅ Recording Finished")
                        break

        audio = np.concatenate(recorded_frames, axis=0)
        sf.write(AUDIO_FILE, audio, SAMPLE_RATE)

        return AUDIO_FILE