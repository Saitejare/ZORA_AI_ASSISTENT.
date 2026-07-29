import webrtcvad


class VoiceActivityDetector:
    def __init__(self, aggressiveness: int = 2) -> None:
        self.vad = webrtcvad.Vad(aggressiveness)

    def is_speech(self, frame: bytes, sample_rate: int) -> bool:
        return self.vad.is_speech(frame, sample_rate)