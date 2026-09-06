import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  getConversation,
  getHealth,
  sendChat,
  sendVoice,
  type ConversationMessage,
  type ZoraHealth,
  type VoiceResponse,
} from "./zoraApi";


/* =========================================================
   CONTEXT TYPE
   ========================================================= */

interface ZoraContextValue {

  health:
    ZoraHealth | null;

  conversation:
    ConversationMessage[];

  error:
    string | null;

  isThinking:
    boolean;

  refresh:
    () => Promise<void>;

  submitMessage:
    (
      message: string,
    ) => Promise<void>;

  submitVoice:
    (
      audioBlob?: Blob,
    ) => Promise<VoiceResponse>;
}


/* =========================================================
   CONTEXT
   ========================================================= */

const ZoraContext =
  createContext<
    ZoraContextValue | null
  >(null);


/* =========================================================
   PROVIDER
   ========================================================= */

export function ZoraProvider({
  children,
}: {
  children: React.ReactNode;
}) {

  const [
    health,
    setHealth,
  ] =
    useState<ZoraHealth | null>(
      null,
    );


  const [
    conversation,
    setConversation,
  ] =
    useState<
      ConversationMessage[]
    >([]);


  const [
    error,
    setError,
  ] =
    useState<string | null>(
      null,
    );


  const [
    isThinking,
    setIsThinking,
  ] =
    useState(false);


  /* =======================================================
     REFRESH
     ======================================================= */

  const refresh =
    useCallback(
      async () => {

        try {

          const [
            nextHealth,
            history,
          ] =
            await Promise.all([
              getHealth(),
              getConversation(),
            ]);


          setHealth(
            nextHealth,
          );


          setConversation(
            history.data ?? [],
          );


          setError(
            null,
          );

        } catch (err) {

          setError(
            err instanceof Error
              ? err.message
              : "Unable to connect to ZORA backend.",
          );
        }

      },
      [],
    );


  /* =======================================================
     TEXT CHAT
     ======================================================= */

  const submitMessage =
    useCallback(
      async (
        message: string,
      ) => {

        const text =
          message.trim();


        if (!text) {
          return;
        }


        setIsThinking(
          true,
        );


        setError(
          null,
        );


        try {

          const result =
            await sendChat(
              text,
            );


          /*
           * Synchronize with backend
           * conversation history.
           */

          await refresh();


          /*
           * Fallback in case the backend
           * conversation history does not
           * immediately contain the response.
           */

          setConversation(
            (previous) => {

              const exists =
                previous.some(
                  (item) =>
                    item.role ===
                      "assistant" &&
                    item.content ===
                      result.response,
                );


              if (exists) {
                return previous;
              }


              return [
                ...previous,

                {
                  role: "assistant",

                  content:
                    result.response,

                  timestamp:
                    new Date()
                      .toISOString(),
                },
              ];
            },
          );

        } catch (err) {

          setError(
            err instanceof Error
              ? err.message
              : "ZORA could not process the request.",
          );

          throw err;

        } finally {

          setIsThinking(
            false,
          );
        }

      },
      [
        refresh,
      ],
    );


  /* =======================================================
     VOICE
     ======================================================= */

  const submitVoice =
    useCallback(
      async (
        audioBlob?: Blob,
      ): Promise<VoiceResponse> => {

        setIsThinking(
          true,
        );


        setError(
          null,
        );


        try {

          console.log(
            "🎤 Sending voice request...",
          );


          /*
           * audioBlob is optional.
           *
           * Normal ZORA operation:
           *
           * submitVoice()
           *
           * Backend records directly
           * from the laptop microphone.
           */

          const result =
            await sendVoice(
              audioBlob,
            );


          console.log(
            "🗣 Transcript:",
            result.transcript,
          );


          console.log(
            "🤖 Response:",
            result.response,
          );


          console.log(
            "🔊 Audio:",
            result.audio,
          );


          /*
           * Synchronize UI with the
           * backend conversation.
           */

          await refresh();


          return result;

        } catch (err) {

          const message =
            err instanceof Error
              ? err.message
              : "ZORA could not process the voice request.";


          console.error(
            "❌ Voice request failed:",
            message,
          );


          setError(
            message,
          );


          throw err;

        } finally {

          setIsThinking(
            false,
          );
        }

      },
      [
        refresh,
      ],
    );


  /* =======================================================
     INITIAL LOAD
     ======================================================= */

  useEffect(
    () => {

      void refresh();

    },
    [
      refresh,
    ],
  );


  /* =======================================================
     CONTEXT VALUE
     ======================================================= */

  const value =
    useMemo(
      () => ({

        health,

        conversation,

        error,

        isThinking,

        refresh,

        submitMessage,

        submitVoice,

      }),
      [

        health,

        conversation,

        error,

        isThinking,

        refresh,

        submitMessage,

        submitVoice,

      ],
    );


  return (

    <ZoraContext.Provider
      value={value}
    >

      {children}

    </ZoraContext.Provider>
  );
}


/* =========================================================
   HOOK
   ========================================================= */

export function useZora() {

  const context =
    useContext(
      ZoraContext,
    );


  if (!context) {

    throw new Error(
      "useZora must be used inside ZoraProvider.",
    );
  }


  return context;
}