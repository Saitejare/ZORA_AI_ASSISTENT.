import time

from backend.audio.player import AudioPlayer
from backend.llm.service import LLMService
from backend.memory.service import MemoryService
from backend.speech.record import SpeechRecorder
from backend.speech.transcribe import SpeechTranscriber
from backend.tools.service import ToolService
from backend.tts.synthesizer import SpeechSynthesizer


def main():

    recorder = SpeechRecorder()
    transcriber = SpeechTranscriber()

    memory = MemoryService()
    zora = LLMService()
    tools = ToolService()

    synthesizer = SpeechSynthesizer()
    player = AudioPlayer()

    print("=" * 50)
    print("          ZORA AI Assistant")
    print("=" * 50)

    while True:

        print("\n🎤 Waiting for speech...")

        audio_path = recorder.record()

        text = transcriber.transcribe(audio_path)

        if not text:
            print("❌ No speech detected.")
            continue

        print(f"\n🧑 You : {text}")

        # ---------------------------------------
        # Memory Recall
        # ---------------------------------------

        recall_start = time.perf_counter()

        memories = memory.recall(text)

        recall_time = time.perf_counter() - recall_start

        memory_context = ""

        if memories:

            memory_context = "\n".join(
                item["text"] for item in memories
            )

            print("\n📚 Relevant Memories:")

            for item in memories:
                print(f" • {item['text']} ({item['score']:.2f})")

        print(f"🧠 Memory Recall Time : {recall_time:.2f} sec")

        # ---------------------------------------
        # Tool Detection
        # ---------------------------------------

        tool_start = time.perf_counter()

        tool_response = tools.handle(text)

        tool_time = time.perf_counter() - tool_start

        print(f"🛠 Tool Detection Time : {tool_time:.2f} sec")

        # ---------------------------------------
        # Tool Executed
        # ---------------------------------------

        if tool_response is not None:

            response = tool_response

            print("\n🛠 Tool Executed")

        else:

            # ---------------------------------------
            # LLM
            # ---------------------------------------

            llm_start = time.perf_counter()

            response = zora.chat(
                text,
                memory_context,
            )

            llm_time = time.perf_counter() - llm_start

            print(f"⚡ LLM Time : {llm_time:.2f} sec")

        print(f"\n🤖 ZORA : {response}")

        # ---------------------------------------
        # Save Memory
        # ---------------------------------------

        memory.remember(text)

        # ---------------------------------------
        # TTS
        # ---------------------------------------

        tts_start = time.perf_counter()

        audio, sample_rate = synthesizer.synthesize(response)

        tts_time = time.perf_counter() - tts_start

        print(f"🔊 TTS Time : {tts_time:.2f} sec")

        # ---------------------------------------
        # Playback
        # ---------------------------------------

        play_start = time.perf_counter()

        player.play(audio, sample_rate)

        play_time = time.perf_counter() - play_start

        print(f"▶ Playback Time : {play_time:.2f} sec")


if __name__ == "__main__":
    main()