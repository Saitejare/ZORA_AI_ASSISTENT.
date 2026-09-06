const API_BASE_URL =
  import.meta.env.VITE_ZORA_API_URL ??
  "http://127.0.0.1:8000";

export { API_BASE_URL };


/* =========================================================
   TYPES
   ========================================================= */

export interface ConversationMessage {
  role: string;
  content: string;
  timestamp?: string;
  tool_calls?: unknown[];
  memory_references?: unknown[];
}


export interface ZoraApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
}


export interface ZoraHealth {
  status: string;
  initialized: boolean;
  version: string;
}


export interface ZoraReadyResponse {
  ready: boolean;
}


export interface MicrophoneReadyResponse {
  ready: boolean;
  microphone: boolean;
}


export interface VoiceAudio {
  sample_rate: number;
  audio_file: string | null;
  media_type?: string;
}


export interface VoiceResponse {
  transcript: string;
  response: string;
  audio: VoiceAudio;
}


/* =========================================================
   GENERIC REQUEST
   ========================================================= */

async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {

  const response =
    await fetch(
      `${API_BASE_URL}${path}`,
      {
        ...options,

        headers: {
          "Content-Type":
            "application/json",

          ...(options?.headers ?? {}),
        },
      },
    );


  if (!response.ok) {

    let errorMessage =
      `Request failed (${response.status})`;


    try {

      const body =
        await response.json();


      if (
        body &&
        typeof body.detail === "string"
      ) {

        errorMessage =
          body.detail;
      }

    } catch {
      // Keep default error.
    }


    throw new Error(
      errorMessage,
    );
  }


  return response.json() as Promise<T>;
}


/* =========================================================
   HEALTH
   ========================================================= */

export function getHealth() {

  return request<ZoraHealth>(
    "/health",
  );
}


/* =========================================================
   ZORA READY
   ========================================================= */

/* =========================================================
   READY
   ========================================================= */

export interface ZoraReadyResponse {
  success: boolean;
  message: string;
  data?: {
    ready: boolean;
  };
}


export async function getReady(): Promise<ZoraReadyResponse> {

  return request<ZoraReadyResponse>(
    "/ready",
  );
}

/* =========================================================
   MICROPHONE INITIALIZATION
   ========================================================= */

export async function initializeMicrophone() {

  const response =
    await request<
      ZoraApiResponse<MicrophoneReadyResponse>
    >(
      "/microphone/initialize",
      {
        method: "POST",

        body:
          JSON.stringify({}),
      },
    );


  if (
    !response.data?.ready ||
    !response.data?.microphone
  ) {

    throw new Error(
      "ZORA microphone could not be initialized.",
    );
  }


  return response.data;
}


/* =========================================================
   CHAT
   ========================================================= */

export async function sendChat(
  message: string,
) {

  const response =
    await request<
      ZoraApiResponse<{
        response: string;
      }>
    >(
      "/chat",
      {
        method: "POST",

        body:
          JSON.stringify({
            message,
          }),
      },
    );


  if (!response.data) {

    throw new Error(
      "Chat response did not contain data.",
    );
  }


  return response.data;
}


/* =========================================================
   VOICE
   ========================================================= */

export async function sendVoice(
  audioBlob?: Blob,
): Promise<VoiceResponse> {

  /*
   * Normal ZORA mode:
   *
   * No audioBlob
   *
   * Backend microphone is used.
   */

  if (!audioBlob) {

    const response =
      await request<
        ZoraApiResponse<VoiceResponse>
      >(
        "/voice",
        {
          method: "POST",

          body:
            JSON.stringify({
              audio_path: null,
            }),
        },
      );


    if (!response.data) {

      throw new Error(
        "Voice response did not contain data.",
      );
    }


    return response.data;
  }


  /*
   * Browser audio mode.
   */

  const formData =
    new FormData();


  formData.append(
    "audio",
    audioBlob,
    "recording.webm",
  );


  const response =
    await fetch(
      `${API_BASE_URL}/voice`,
      {
        method: "POST",

        body: formData,
      },
    );


  if (!response.ok) {

    let errorMessage =
      `Voice request failed (${response.status})`;


    try {

      const body =
        await response.json();


      if (
        body &&
        typeof body.detail === "string"
      ) {

        errorMessage =
          body.detail;
      }

    } catch {
      // Keep default error.
    }


    throw new Error(
      errorMessage,
    );
  }


  const result =
    await response.json() as
      ZoraApiResponse<VoiceResponse>;


  if (!result.data) {

    throw new Error(
      "Voice response did not contain data.",
    );
  }


  return result.data;
}


/* =========================================================
   CONVERSATION
   ========================================================= */

export function getConversation() {

  return request<
    ZoraApiResponse<
      ConversationMessage[]
    >
  >(
    "/conversation",
  );
}


/* =========================================================
   LATEST AUDIO
   ========================================================= */

export async function playLatestAudio(): Promise<void> {

  const audio =
    new Audio(
      `${API_BASE_URL}/audio/latest?t=${Date.now()}`,
    );


  audio.preload =
    "auto";


  await audio.play();


  await new Promise<void>(
    (
      resolve,
      reject,
    ) => {

      audio.onended =
        () => {
          resolve();
        };


      audio.onerror =
        () => {

          reject(
            new Error(
              "Unable to play ZORA audio.",
            ),
          );
        };

    },
  );
}