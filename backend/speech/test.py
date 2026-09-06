import speech_recognition as sr
import pyttsx3


def speak(text: str):

    print("🔊 Speaking:")
    print(text)

    engine = pyttsx3.init()

    voices = engine.getProperty("voices")

    if voices:

        if len(voices) > 1:
            engine.setProperty(
                "voice",
                voices[1].id
            )
        else:
            engine.setProperty(
                "voice",
                voices[0].id
            )

    engine.setProperty(
        "rate",
        170
    )

    engine.say(text)
    engine.runAndWait()


def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print()
        print("🎤 Listening...")

        recognizer.pause_threshold = 1

        print("🎧 Adjusting microphone...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        print("🎤 Speak now...")

        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=10
        )

    print("✅ Recording finished")

    try:

        print("🧠 Recognizing...")

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print()
        print("🗣 You said:")
        print(text)

        return text

    except sr.UnknownValueError:

        print("❌ Could not understand the speech.")
        return ""

    except sr.RequestError as exc:

        print("❌ Speech recognition service error:")
        print(exc)

        return ""


def main():

    print("=" * 50)
    print("     ZORA VOICE TEST")
    print("=" * 50)

    text = listen()

    if not text:
        return

    print()
    print("=" * 50)
    print("TEXT-TO-SPEECH TEST")
    print("=" * 50)

    speak(
        f"You said: {text}"
    )

    print()
    print("✅ Voice test completed.")


if __name__ == "__main__":
    main()