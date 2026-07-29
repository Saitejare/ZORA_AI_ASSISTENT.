from .vad import VoiceActivityDetector

def main():
    vad = VoiceActivityDetector()
    print("WebRTC VAD Loaded Successfully")

if __name__ == "__main__":
    main()