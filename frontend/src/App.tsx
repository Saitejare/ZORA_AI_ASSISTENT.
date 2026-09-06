import React, {
  FormEvent,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import { HolographicParticles } from "./components/Background/HolographicParticles";
import { FaceContainer } from "./components/Face/FaceContainer";
import { StatusIndicators } from "./components/HUD/StatusIndicators";
import { SystemStats } from "./components/HUD/SystemStats";
import { TopNav } from "./components/HUD/TopNav";
import { NotificationStack } from "./components/Notifications/NotificationStack";
import { VoiceWaveform } from "./components/Waveform/VoiceWaveform";

import { useAudioLevel } from "./hooks/useAudioLevel";
import { useMicrophoneLevel } from "./hooks/useMicrophoneLevel";
import { useSystemStats } from "./hooks/useSystemStats";

import {
  API_BASE_URL,
  getReady,
  initializeMicrophone,
} from "./services/zoraApi";

import {
  ZoraProvider,
  useZora,
} from "./services/ZoraContext";

import type {
  NotificationItem,
  ZoraState,
} from "./types";


/* =========================================================
   CONSTANTS
   ========================================================= */

const STARTUP_MESSAGE =
  "Hello, Sai Teja. I am ZORA, your AI assistant. How can I help you today?";


const READY_POLL_INTERVAL = 300;

const VOICE_RETRY_DELAY = 500;


/* =========================================================
   RESPONSE MOOD
   ========================================================= */

function detectResponseMood(
  text: string,
): ZoraState {

  const value =
    text
      .toLowerCase()
      .trim();


  const angryIndicators = [
    "angry",
    "frustrated",
    "annoyed",
    "upset",
    "error",
    "failed",
    "cannot",
    "can't",
    "unable",
    "couldn't",
    "could not",
    "sorry",
  ];


  const happyIndicators = [
    "great",
    "excellent",
    "success",
    "successfully",
    "done",
    "completed",
    "perfect",
    "congratulations",
    "happy",
    "glad",
    "wonderful",
  ];


  const curiousIndicators = [
    "?",
    "why",
    "how",
    "what",
    "which",
    "where",
    "when",
    "who",
  ];


  if (
    angryIndicators.some(
      (word) =>
        value.includes(word),
    )
  ) {

    return "Angry" as ZoraState;
  }


  if (
    happyIndicators.some(
      (word) =>
        value.includes(word),
    )
  ) {

    return "Happy" as ZoraState;
  }


  if (
    curiousIndicators.some(
      (word) =>
        value.includes(word),
    )
  ) {

    return "Curious" as ZoraState;
  }


  return "Idle";
}


/* =========================================================
   MAIN EXPERIENCE
   ========================================================= */

function ZoraExperience() {

  const {
    conversation,
    error,
    health,
    isThinking,
    submitMessage,
    submitVoice,
  } = useZora();


  /* =======================================================
     STATE
     ======================================================= */

  const [
    currentState,
    setCurrentState,
  ] =
    useState<ZoraState>("Idle");


  const [
    message,
    setMessage,
  ] =
    useState("");


  const [
    backendReady,
    setBackendReady,
  ] =
    useState(false);


  const [
    microphoneReady,
    setMicrophoneReady,
  ] =
    useState(false);


  const [
    startupComplete,
    setStartupComplete,
  ] =
    useState(false);


  /* =======================================================
     REFS
     ======================================================= */

  const mountedRef =
    useRef(true);


  const startupRunningRef =
    useRef(false);


  const voiceRunningRef =
    useRef(false);


  const audioRef =
    useRef<HTMLAudioElement | null>(null);


  const voiceRetryTimerRef =
    useRef<number | null>(null);


  /* =======================================================
     SYSTEM
     ======================================================= */

  const stats =
    useSystemStats();


  const simulatedAudioLevel =
    useAudioLevel(currentState);


  const microphone =
    useMicrophoneLevel();


  const audioLevel =
    microphone.isActive
      ? microphone.audioLevel
      : simulatedAudioLevel;


  /* =======================================================
     NOTIFICATIONS
     ======================================================= */

  const notifications =
    useMemo<NotificationItem[]>(
      () => [

        {
          id: "1",

          title:
            "ZORA Neural Engine",

          message:
            !backendReady
              ? "Waiting for ZORA backend..."
              : !microphoneReady
                ? "Initializing microphone..."
                : !startupComplete
                  ? "Preparing ZORA..."
                  : "All systems ready. Voice interaction active.",

          type:
            backendReady &&
            microphoneReady &&
            startupComplete
              ? "success"
              : "warning",

          timestamp:
            "12:00:04",
        },


        error
          ? {
              id: "2",

              title:
                "Backend Notice",

              message:
                error,

              type:
                "error",

              timestamp:
                "12:00:05",
            }

          : {
              id: "2",

              title:
                "Conversation Memory",

              message:
                `${conversation.length} messages available from the API.`,

              type:
                "info",

              timestamp:
                "12:00:05",
            },
      ],

      [
        backendReady,
        microphoneReady,
        startupComplete,
        conversation.length,
        error,
      ],
    );


  /* =======================================================
     STOP AUDIO
     ======================================================= */

  const stopCurrentAudio =
    useCallback(
      () => {

        const audio =
          audioRef.current;


        if (!audio) {
          return;
        }


        try {

          audio.pause();

          audio.currentTime =
            0;

          audio.src =
            "";

        } catch {
          // Audio may already be released.
        }


        audioRef.current =
          null;
      },
      [],
    );


  /* =======================================================
     PLAY RESPONSE AUDIO
     ======================================================= */

  const playResponseAudio =
    useCallback(
      async (): Promise<void> => {

        if (!mountedRef.current) {
          return;
        }


        stopCurrentAudio();


        const audioUrl =
          `${API_BASE_URL}/audio/latest?t=${Date.now()}`;


        console.log(
          "🔊 ZORA audio:",
          audioUrl,
        );


        const audio =
          new Audio(audioUrl);


        audio.preload =
          "auto";


        audioRef.current =
          audio;


        await new Promise<void>(
          (
            resolve,
            reject,
          ) => {

            let settled =
              false;


            const finish =
              () => {

                if (settled) {
                  return;
                }


                settled =
                  true;


                if (
                  audioRef.current ===
                  audio
                ) {

                  audioRef.current =
                    null;
                }


                resolve();
              };


            audio.onended =
              finish;


            audio.onerror =
              () => {

                if (settled) {
                  return;
                }


                settled =
                  true;


                if (
                  audioRef.current ===
                  audio
                ) {

                  audioRef.current =
                    null;
                }


                reject(
                  new Error(
                    "Unable to play ZORA audio.",
                  ),
                );
              };


            void audio
              .play()
              .catch(
                (playError) => {

                  if (settled) {
                    return;
                  }


                  settled =
                    true;


                  if (
                    audioRef.current ===
                    audio
                  ) {

                    audioRef.current =
                      null;
                  }


                  reject(
                    playError,
                  );
                },
              );
          },
        );
      },
      [
        stopCurrentAudio,
      ],
    );


  /* =======================================================
     VOICE LOOP
     ======================================================= */

  const listenAutomatically =
    useCallback(
      async () => {

        if (!mountedRef.current) {
          return;
        }


        if (!backendReady) {

          console.log(
            "⏳ Voice waiting for backend...",
          );

          return;
        }


        if (!microphoneReady) {

          console.log(
            "⏳ Voice waiting for microphone...",
          );

          return;
        }


        if (!startupComplete) {

          console.log(
            "⏳ Voice waiting for startup...",
          );

          return;
        }


        if (voiceRunningRef.current) {
          return;
        }


        voiceRunningRef.current =
          true;


        try {

          /* ---------------------------------------------
             LISTENING
             --------------------------------------------- */

          setCurrentState(
            "Listening",
          );


          console.log(
            "🎤 ZORA is listening...",
          );


          /* ---------------------------------------------
             BACKEND VOICE PIPELINE
             --------------------------------------------- */

          const result =
            await submitVoice();


          if (!mountedRef.current) {
            return;
          }


          /* ---------------------------------------------
             EMPTY TRANSCRIPT
             --------------------------------------------- */

          if (
            !result.transcript ||
            !result.transcript.trim()
          ) {

            console.log(
              "⚠️ No speech detected. Listening again...",
            );


            setCurrentState(
              "Listening",
            );


            return;
          }


          console.log(
            "🗣 User:",
            result.transcript,
          );


          console.log(
            "🤖 ZORA:",
            result.response,
          );


          /* ---------------------------------------------
             DETECT MOOD
             --------------------------------------------- */

          const mood =
            detectResponseMood(
              result.response,
            );


          /* ---------------------------------------------
             SPEAKING
             --------------------------------------------- */

          setCurrentState(
            "Speaking",
          );


          /* ---------------------------------------------
             PLAY TTS
             --------------------------------------------- */

          if (
            result.audio?.audio_file
          ) {

            try {

              await playResponseAudio();

            } catch (audioError) {

              console.error(
                "❌ Audio playback failed:",
                audioError,
              );
            }
          }


          if (!mountedRef.current) {
            return;
          }


          /* ---------------------------------------------
             SHOW RESPONSE MOOD
             --------------------------------------------- */

          setCurrentState(
            mood,
          );


          await new Promise<void>(
            (resolve) => {

              window.setTimeout(
                resolve,
                300,
              );
            },
          );

        } catch (err) {

          console.error(
            "❌ Voice interaction failed:",
            err,
          );


          if (mountedRef.current) {

            setCurrentState(
              "Error" as ZoraState,
            );
          }

        } finally {

          voiceRunningRef.current =
            false;


          if (
            mountedRef.current &&
            backendReady &&
            microphoneReady &&
            startupComplete
          ) {

            if (
              voiceRetryTimerRef.current !==
              null
            ) {

              window.clearTimeout(
                voiceRetryTimerRef.current,
              );
            }


            voiceRetryTimerRef.current =
              window.setTimeout(
                () => {

                  voiceRetryTimerRef.current =
                    null;

                  void listenAutomatically();

                },
                VOICE_RETRY_DELAY,
              );
          }
        }
      },
      [
        backendReady,
        microphoneReady,
        playResponseAudio,
        startupComplete,
        submitVoice,
      ],
    );


  /* =======================================================
     STARTUP
     ======================================================= */

  useEffect(
    () => {

      mountedRef.current =
        true;


      if (startupRunningRef.current) {
        return;
      }


      startupRunningRef.current =
        true;


      const waitForBackend =
        async (): Promise<boolean> => {

          console.log(
            "⏳ Waiting for ZORA backend readiness...",
          );


          while (
            mountedRef.current
          ) {

            try {

              const result =await getReady();
              console.log("🔎 ZORA readiness:",result,);
              if (result.success &&result.data?.ready === true) {

                console.log(
                  "✅ ZORA backend is ready.",
                );


                if (
                  mountedRef.current
                ) {

                  setBackendReady(
                    true,
                  );
                }


                return true;
              }

            } catch (err) {

              console.log(
                "⏳ Backend readiness check failed:",
                err,
              );
            }


            await new Promise<void>(
              (resolve) => {

                window.setTimeout(
                  resolve,
                  READY_POLL_INTERVAL,
                );
              },
            );
          }


          return false;
        };


      const startup =
        async () => {

          try {

            /* -------------------------------------------
               STEP 1
               WAIT FOR COMPLETE BACKEND
               ------------------------------------------- */

            const ready =
              await waitForBackend();


            if (
              !ready ||
              !mountedRef.current
            ) {

              return;
            }


            /* -------------------------------------------
               STEP 2
               INITIALIZE MICROPHONE
               ------------------------------------------- */

            console.log(
              "🎤 Initializing microphone...",
            );


            await initializeMicrophone();


            if (!mountedRef.current) {
              return;
            }


            setMicrophoneReady(
              true,
            );


            console.log(
              "✅ Microphone is ready.",
            );


            /* -------------------------------------------
               STEP 3
               BACKEND + MICROPHONE READY
               ------------------------------------------- */

            console.log(
              "✅ ZORA systems ready.",
            );


            /* -------------------------------------------
               STEP 4
               INTRODUCTION
               ------------------------------------------- */

            setCurrentState(
              "Speaking",
            );


            console.log(
              "🤖 ZORA introduction starting...",
            );


            const speakStartup =
              (
                text: string,
              ): Promise<void> => {

                return new Promise<void>(
                  (resolve) => {

                    const utterance =
                      new SpeechSynthesisUtterance(
                        text,
                      );


                    utterance.lang =
                      "en-IN";


                    utterance.rate =
                      0.95;


                    utterance.pitch =
                      1.0;


                    let finished =
                      false;


                    const finish =
                      () => {

                        if (finished) {
                          return;
                        }


                        finished =
                          true;


                        resolve();
                      };


                    utterance.onend =
                      finish;


                    utterance.onerror =
                      finish;


                    window.speechSynthesis.cancel();


                    window.speechSynthesis.speak(
                      utterance,
                    );
                  },
                );
              };


            await speakStartup(
              STARTUP_MESSAGE,
            );


            if (!mountedRef.current) {
              return;
            }


            console.log(
              "✅ ZORA introduction finished.",
            );


            /* -------------------------------------------
               STEP 5
               ONLY NOW ENABLE CONVERSATION
               ------------------------------------------- */

            setStartupComplete(
              true,
            );


            setCurrentState(
              "Listening",
            );


            console.log(
              "🎤 ZORA is now ready for conversation.",
            );

          } catch (err) {

            console.error(
              "❌ ZORA startup failed:",
              err,
            );


            if (
              mountedRef.current
            ) {

              setCurrentState(
                "Error" as ZoraState,
              );
            }

          }
        };


      void startup();


      return () => {

        mountedRef.current =
          false;


        if (
          voiceRetryTimerRef.current !==
          null
        ) {

          window.clearTimeout(
            voiceRetryTimerRef.current,
          );


          voiceRetryTimerRef.current =
            null;
        }


        window.speechSynthesis.cancel();


        stopCurrentAudio();

      };

    },
    [
      stopCurrentAudio,
    ],
  );


  /* =======================================================
     START VOICE AFTER STARTUP
     ======================================================= */

  useEffect(
    () => {

      if (
        !backendReady ||
        !microphoneReady ||
        !startupComplete
      ) {

        return;
      }


      if (
        voiceRunningRef.current
      ) {

        return;
      }


      console.log(
        "🎤 Starting automatic voice conversation...",
      );


      void listenAutomatically();

    },
    [
      backendReady,
      microphoneReady,
      startupComplete,
      listenAutomatically,
    ],
  );


  /* =======================================================
     TEXT CHAT
     ======================================================= */

  const handleSubmit =
    useCallback(
      (
        event: FormEvent<HTMLFormElement>,
      ) => {

        event.preventDefault();


        const value =
          message.trim();


        if (!value) {
          return;
        }


        stopCurrentAudio();


        setCurrentState(
          "Thinking",
        );


        void submitMessage(
          value,
        )
          .then(
            () => {

              setCurrentState(
                "Idle",
              );
            },
          )
          .catch(
            () => {

              setCurrentState(
                "Error" as ZoraState,
              );
            },
          )
          .finally(
            () => {

              setMessage("");

            },
          );

      },
      [
        message,
        stopCurrentAudio,
        submitMessage,
      ],
    );


  /* =======================================================
     LATEST ASSISTANT MESSAGE
     ======================================================= */

  const latestAssistantMessage =
    [...conversation]
      .reverse()
      .find(
        (item) =>
          item.role ===
          "assistant",
      );


  /* =======================================================
     UI
     ======================================================= */

  return (

    <div className="zora-shell">

      {/* =================================================
          BACKGROUND
          ================================================= */}

      <HolographicParticles
        state={currentState}
      />


      {/* =================================================
          HEADER
          ================================================= */}

      <header className="zora-header">

        <TopNav />


        <StatusIndicators
          stats={{
            ...stats,

            microphone:
              microphoneReady &&
              currentState ===
                "Listening",
          }}
        />

      </header>


      {/* =================================================
          MAIN
          ================================================= */}

      <main className="zora-main">

        <FaceContainer
          state={currentState}
          audioLevel={audioLevel}
        />


        <VoiceWaveform
          audioLevel={audioLevel}
          state={currentState}
        />


        {/* =================================================
            CONVERSATION
            ================================================= */}

        <section
          className="conversation-panel no-drag"
        >

          <div
            className="conversation-panel__history"
          >

            {conversation
              .slice(-4)
              .map(
                (
                  item,
                  index,
                ) => (

                  <p
                    key={
                      `${item.timestamp ?? index}-${item.role}-${index}`
                    }

                    className={
                      `conversation-panel__message ` +
                      `conversation-panel__message--${item.role}`
                    }
                  >

                    <span>
                      {item.role}
                    </span>

                    {item.content}

                  </p>

                ),
              )}


            {!conversation.length && (

              <p
                className="conversation-panel__empty"
              >

                {!backendReady
                  ? "Connecting to ZORA..."

                  : !microphoneReady
                    ? "Preparing microphone..."

                    : !startupComplete
                      ? "ZORA is preparing..."

                      : currentState ===
                        "Listening"
                        ? "ZORA is listening..."

                        : currentState ===
                          "Speaking"
                          ? "ZORA is speaking..."

                          : "ZORA is ready."}

              </p>

            )}

          </div>


          {/* =================================================
              TEXT INPUT
              ================================================= */}

          <form
            className="conversation-panel__form"
            onSubmit={
              handleSubmit
            }
          >

            <input
              value={
                message
              }

              onChange={
                (
                  event,
                ) =>
                  setMessage(
                    event.target.value,
                  )
              }

              placeholder={
                latestAssistantMessage?.content
                  ? "Reply to ZORA..."
                  : "Ask ZORA anything..."
              }

              aria-label="Message ZORA"

              disabled={
                isThinking
              }
            />


            <button
              type="submit"

              disabled={
                isThinking ||
                !message.trim()
              }
            >

              {isThinking
                ? "THINKING"
                : "SEND"}

            </button>

          </form>

        </section>

      </main>


      {/* =================================================
          FOOTER
          ================================================= */}

      <footer
        className="zora-footer"
      >

        <SystemStats
          stats={stats}
        />


        <div
          className="zora-footer__controls"
        >

          <div
            className="voice-control no-drag"
            aria-live="polite"
          >

            VOICE:


            <span>

              {!backendReady

                ? "STARTING"

                : !microphoneReady

                  ? "MIC INITIALIZING"

                  : !startupComplete

                    ? "PREPARING"

                    : currentState ===
                      "Listening"

                      ? "LISTENING"

                      : currentState ===
                        "Thinking"

                        ? "PROCESSING"

                        : currentState ===
                          "Speaking"

                          ? "SPEAKING"

                          : currentState ===
                            "Error"

                            ? "ERROR"

                            : "READY"}

            </span>


            <small>

              {microphone.error ??

                (!backendReady

                  ? "Waiting for ZORA backend..."

                  : !microphoneReady

                    ? "Initializing microphone..."

                    : !startupComplete

                      ? "Preparing introduction..."

                      : currentState ===
                        "Listening"

                        ? "Listening automatically..."

                        : currentState ===
                          "Speaking"

                          ? "ZORA is speaking..."

                          : currentState ===
                            "Thinking"

                            ? "Processing request..."

                            : "Voice interaction active")}

            </small>

          </div>

        </div>

      </footer>


      {/* =================================================
          NOTIFICATIONS
          ================================================= */}

      <NotificationStack
        notifications={
          notifications
        }
      />

    </div>
  );
}


/* =========================================================
   APP
   ========================================================= */

export default function App() {

  return (

    <ZoraProvider>

      <ZoraExperience />

    </ZoraProvider>
  );
}