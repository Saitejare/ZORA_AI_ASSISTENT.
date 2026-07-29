from .record import SpeechRecorder
from .transcribe import SpeechTranscriber


def main():
    recorder = SpeechRecorder()

    audio_path = recorder.record()

    transcriber = SpeechTranscriber()

    text = transcriber.transcribe(audio_path)

    print("\nRecognized Text:")
    print(text)


if __name__ == "__main__":
    main()