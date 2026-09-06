import React from "react";
import { motion } from "framer-motion";

interface AudioMouthProps {
  audioLevel: number;
  state: string;
}

export const AudioMouth: React.FC<AudioMouthProps> = React.memo(
  ({ audioLevel, state }) => {

    const isError =
      state === "Error";

    const isHappy =
      state === "Happy";

    /*
     * IMPORTANT:
     *
     * The mouth should NOT animate continuously
     * while ZORA is only listening.
     *
     * Mouth animation is active only while
     * ZORA is actually speaking.
     */
    const isSpeaking =
      state === "Speaking";


    const primaryColor =
      isError
        ? "#ff5500"
        : "#00f0ff";


    /*
     * Keep audioLevel safely between 0 and 1.
     */
    const level =
      Math.max(
        0,
        Math.min(
          1,
          Number.isFinite(audioLevel)
            ? audioLevel
            : 0,
        ),
      );


    /*
     * Mouth dimensions.
     *
     * Speaking:
     *     React to actual audio level.
     *
     * Happy:
     *     Static smile.
     *
     * Everything else:
     *     Nearly closed.
     */
    const mouthOpenHeight =
      isSpeaking
        ? 4 + level * 32
        : isHappy
          ? 12
          : 3;


    const mouthWidth =
      isSpeaking
        ? 38 + level * 22
        : isHappy
          ? 50
          : 40;


    const leftCornerX =
      200 - mouthWidth / 2;


    const rightCornerX =
      200 + mouthWidth / 2;


    /*
     * Speaking mouth path.
     */
    const upperMouthPath =
      `M ${leftCornerX} 0 ` +
      `Q 200 ${-mouthOpenHeight / 2} ` +
      `${rightCornerX} 0`;


    const lowerMouthPath =
      `M ${leftCornerX} 0 ` +
      `Q 200 ${mouthOpenHeight} ` +
      `${rightCornerX} 0`;


    /*
     * Idle / listening mouth.
     *
     * This stays stable while ZORA listens.
     */
    const idleMouthPath =
      `M ${leftCornerX} 0 ` +
      `Q 200 3 ` +
      `${rightCornerX} 0`;


    /*
     * Happy smile.
     */
    const happyMouthPath =
      `M ${leftCornerX} 0 ` +
      `Q 200 ${-mouthOpenHeight} ` +
      `${rightCornerX} 0`;


    return (
      <g
        id="holographic-mouth"
        transform="translate(0, 275)"
      >

        {/* =================================================
            MAIN MOUTH
            ================================================= */}

        <motion.path
          stroke={primaryColor}
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          opacity="0.9"

          d={
            isSpeaking
              ? upperMouthPath
              : isHappy
                ? happyMouthPath
                : idleMouthPath
          }

          animate={{
            d:
              isSpeaking
                ? upperMouthPath
                : isHappy
                  ? happyMouthPath
                  : idleMouthPath,
          }}

          transition={{
            duration:
              isSpeaking
                ? 0.06
                : 0.18,

            ease:
              "easeOut",
          }}
        />


        {/* =================================================
            LOWER MOUTH
            ================================================= */}

        <motion.path
          stroke={primaryColor}
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          opacity={
            isSpeaking
              ? 0.9
              : 0
          }

          d={
            isSpeaking
              ? lowerMouthPath
              : idleMouthPath
          }

          animate={{
            d:
              isSpeaking
                ? lowerMouthPath
                : idleMouthPath,

            opacity:
              isSpeaking
                ? 0.9
                : 0,
          }}

          transition={{
            duration:
              isSpeaking
                ? 0.06
                : 0.15,

            ease:
              "easeOut",
          }}
        />


        {/* =================================================
            SPEAKING AUDIO GLOW
            ================================================= */}

        {isSpeaking && (

          <motion.ellipse
            cx="200"

            cy={
              mouthOpenHeight / 4
            }

            rx={
              mouthWidth / 3
            }

            ry={
              Math.max(
                1,
                mouthOpenHeight / 3,
              )
            }

            fill={primaryColor}

            initial={{
              opacity: 0,
              scale: 0.9,
            }}

            animate={{
              opacity:
                0.25 +
                level * 0.45,

              scale:
                0.95 +
                level * 0.15,
            }}

            transition={{
              duration: 0.06,
              ease: "easeOut",
            }}
          />

        )}

      </g>
    );
  },
);


AudioMouth.displayName =
  "AudioMouth";