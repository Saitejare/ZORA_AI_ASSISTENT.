"""
Production-grade text normalization for ZORA speech output.

The LLM response can contain Markdown, tables, emojis, URLs,
Unicode formatting artifacts, and other characters that are
useful on screen but unnatural when spoken.

This module converts the response into natural speech text
without changing the original response shown in the UI.
"""

from __future__ import annotations

import re
import unicodedata


# =========================================================
# EMOJI / SYMBOL TRANSLATIONS
# =========================================================

EMOJI_REPLACEMENTS: dict[str, str] = {

    # Positive / happy
    "😀": "That sounds positive.",
    "😃": "That sounds positive.",
    "😄": "That sounds great.",
    "😁": "That sounds great.",
    "😆": "That's funny.",
    "😊": "That's nice.",
    "🙂": "That sounds good.",
    "🙃": "That's interesting.",
    "😉": "That's a good one.",
    "😍": "That's wonderful.",
    "🥰": "That's wonderful.",
    "😘": "That's sweet.",
    "🤗": "That's great.",
    "🎉": "That's great news.",
    "🥳": "That's something to celebrate.",
    "👏": "Well done.",
    "👍": "Sounds good.",
    "👌": "Perfect.",
    "💯": "Excellent.",

    # Thinking / information
    "🤔": "That's something to think about.",
    "💡": "Here's an idea.",
    "🧠": "Here's an important point.",
    "📌": "Important point.",
    "ℹ️": "Information.",

    # Warning / error
    "⚠️": "Warning.",
    "⚠": "Warning.",
    "❗": "Important.",
    "❕": "Important.",
    "❌": "This failed.",
    "✖️": "This failed.",
    "✖": "This failed.",
    "🚫": "This is not allowed.",

    # Success
    "✅": "Completed successfully.",
    "✔️": "Completed successfully.",
    "✔": "Completed successfully.",
    "☑️": "Completed.",

    # Questions
    "❓": "Question.",
    "❔": "Question.",

    # Work / technology
    "💻": "Computer.",
    "🖥️": "Computer.",
    "📱": "Phone.",
    "⌨️": "Keyboard.",
    "🖱️": "Mouse.",
    "📂": "Folder.",
    "📁": "Folder.",
    "📄": "File.",
    "🔧": "Tool.",
    "⚙️": "Settings.",

    # Common numbered emojis
    "1️⃣": "Step one.",
    "2️⃣": "Step two.",
    "3️⃣": "Step three.",
    "4️⃣": "Step four.",
    "5️⃣": "Step five.",
    "6️⃣": "Step six.",
    "7️⃣": "Step seven.",
    "8️⃣": "Step eight.",
    "9️⃣": "Step nine.",
    "🔟": "Step ten.",

    # Arrows
    "➡️": "Next.",
    "⬅️": "Previous.",
    "⬆️": "Up.",
    "⬇️": "Down.",
    "→": "to",
    "←": "from",
    "↑": "up",
    "↓": "down",

    # Miscellaneous
    "❤️": "Love.",
    "♥️": "Love.",
    "🔥": "That's impressive.",
    "✨": "That's special.",
    "⭐": "Excellent.",
    "🌟": "Excellent.",
    "🚀": "Let's move forward.",
    "🎯": "The goal.",
    "🔒": "Secure.",
    "🔓": "Unlocked.",
}


# =========================================================
# UNICODE NORMALIZATION
# =========================================================

def _normalize_unicode(text: str) -> str:
    """
    Normalize Unicode and remove control characters while
    preserving useful punctuation.
    """

    text = unicodedata.normalize(
        "NFKC",
        text,
    )

    cleaned: list[str] = []

    for char in text:

        category = unicodedata.category(char)

        if category.startswith("C"):

            if char in "\n\r\t":

                cleaned.append(char)

            continue

        cleaned.append(char)

    return "".join(cleaned)


# =========================================================
# EMOJI REPLACEMENT
# =========================================================

def _replace_emojis(text: str) -> str:
    """
    Convert known emojis into short natural-language phrases.
    """

    for emoji, replacement in sorted(
        EMOJI_REPLACEMENTS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):

        text = text.replace(
            emoji,
            f" {replacement} ",
        )

    return text


# =========================================================
# REMOVE UNKNOWN EMOJIS
# =========================================================

def _remove_remaining_symbols(text: str) -> str:
    """
    Remove remaining emoji-like Unicode symbols that do not
    have a useful spoken representation.

    Normal English punctuation is preserved.
    """

    result: list[str] = []

    for char in text:

        category = unicodedata.category(char)

        codepoint = ord(char)

        # Unicode symbol ranges commonly containing emoji.
        is_emoji_range = (
            0x1F000 <= codepoint <= 0x1FAFF
            or 0x2600 <= codepoint <= 0x27BF
            or 0xFE00 <= codepoint <= 0xFE0F
            or 0x1F3FB <= codepoint <= 0x1F3FF
        )

        if is_emoji_range:

            continue

        if category == "So":

            continue

        result.append(char)

    return "".join(result)


# =========================================================
# MARKDOWN CODE BLOCKS
# =========================================================

def _remove_code_blocks(text: str) -> str:
    """
    Prevent long code blocks from being read literally.

    Short inline code is handled separately.
    """

    text = re.sub(
        r"```[\s\S]*?```",
        " The code is shown in the application. ",
        text,
    )

    return text


# =========================================================
# MARKDOWN LINKS
# =========================================================

def _clean_links(text: str) -> str:
    """
    Convert Markdown links to readable link text and prevent
    raw URLs from being spoken character-by-character.
    """

    # [Google](https://google.com)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )

    # Bare URLs
    text = re.sub(
        r"https?://\S+",
        "the provided link",
        text,
        flags=re.IGNORECASE,
    )

    # www.example.com
    text = re.sub(
        r"\bwww\.[^\s]+",
        "the provided website",
        text,
        flags=re.IGNORECASE,
    )

    return text


# =========================================================
# MARKDOWN HEADINGS
# =========================================================

def _clean_headings(text: str) -> str:

    text = re.sub(
        r"(?m)^\s{0,3}#{1,6}\s*",
        "",
        text,
    )

    return text


# =========================================================
# MARKDOWN EMPHASIS
# =========================================================

def _clean_emphasis(text: str) -> str:

    text = re.sub(
        r"\*\*\*(.*?)\*\*\*",
        r"\1",
        text,
        flags=re.DOTALL,
    )

    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        text,
        flags=re.DOTALL,
    )

    text = re.sub(
        r"__(.*?)__",
        r"\1",
        text,
        flags=re.DOTALL,
    )

    text = re.sub(
        r"(?<!\*)\*([^*\n]+)\*(?!\*)",
        r"\1",
        text,
    )

    text = re.sub(
        r"(?<!_)_([^_\n]+)_(?!_)",
        r"\1",
        text,
    )

    return text


# =========================================================
# INLINE CODE
# =========================================================

def _clean_inline_code(text: str) -> str:

    text = re.sub(
        r"`([^`]+)`",
        r"\1",
        text,
    )

    return text


# =========================================================
# HORIZONTAL RULES
# =========================================================

def _remove_horizontal_rules(text: str) -> str:

    text = re.sub(
        r"(?m)^\s*[-*_]{3,}\s*$",
        "",
        text,
    )

    text = re.sub(
        r"(?m)^\s*-{3,}\s*$",
        "",
        text,
    )

    return text


# =========================================================
# MARKDOWN TABLES
# =========================================================

def _convert_tables(text: str) -> str:
    """
    Convert Markdown tables into speech-friendly sentences.
    """

    lines = text.splitlines()

    output: list[str] = []

    table_rows: list[list[str]] = []

    def flush_table() -> None:

        nonlocal table_rows

        if not table_rows:
            return

        if len(table_rows) == 1:

            row = table_rows[0]

            if row:

                output.append(
                    ". ".join(row) + "."
                )

            table_rows = []

            return

        headers = table_rows[0]

        body = table_rows[1:]

        for row in body:

            cells = [
                cell
                for cell in row
                if cell.strip()
            ]

            if not cells:
                continue

            if headers:

                parts: list[str] = []

                for index, value in enumerate(
                    cells
                ):

                    if index < len(headers):

                        header = headers[index].strip()

                        if header:

                            parts.append(
                                f"{header}: {value}"
                            )

                        else:

                            parts.append(value)

                    else:

                        parts.append(value)

                sentence = ", ".join(parts)

            else:

                sentence = ", ".join(cells)

            output.append(
                sentence + "."
            )

        table_rows = []

    for line in lines:

        stripped = line.strip()

        if (
            stripped.startswith("|")
            and stripped.endswith("|")
        ):

            cells = [
                cell.strip()
                for cell in stripped.strip("|").split("|")
            ]

            # Markdown separator row
            if all(
                re.fullmatch(
                    r":?-{2,}:?",
                    cell,
                )
                for cell in cells
                if cell
            ):

                continue

            table_rows.append(cells)

            continue

        flush_table()

        output.append(line)

    flush_table()

    return "\n".join(output)


# =========================================================
# BULLET LISTS
# =========================================================

def _clean_bullets(text: str) -> str:

    text = re.sub(
        r"(?m)^\s*[-*+]\s+",
        "",
        text,
    )

    text = re.sub(
        r"(?m)^\s*\d+\.\s+",
        "",
        text,
    )

    return text


# =========================================================
# SPECIAL MARKDOWN CHARACTERS
# =========================================================

def _clean_markdown_characters(text: str) -> str:

    text = text.replace(
        "```",
        "",
    )

    text = text.replace(
        "---",
        " ",
    )

    text = text.replace(
        "___",
        " ",
    )

    text = text.replace(
        "***",
        " ",
    )

    text = text.replace(
        "∩┐╜",
        "",
    )

    text = text.replace(
        "�",
        "",
    )

    return text


# =========================================================
# SPEECH PUNCTUATION
# =========================================================

def _normalize_punctuation(text: str) -> str:

    # Remove repeated punctuation.
    text = re.sub(
        r"[.]{3,}",
        ".",
        text,
    )

    text = re.sub(
        r"[!]{2,}",
        "!",
        text,
    )

    text = re.sub(
        r"[?]{2,}",
        "?",
        text,
    )

    # Remove repeated dashes.
    text = re.sub(
        r"-{2,}",
        " ",
        text,
    )

    # Remove decorative pipes.
    text = re.sub(
        r"\|+",
        " ",
        text,
    )

    # Remove decorative tilde.
    text = re.sub(
        r"~{2,}",
        " ",
        text,
    )

    # Normalize whitespace.
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


# =========================================================
# FIX COMMON ENCODING ARTIFACTS
# =========================================================

def _fix_encoding_artifacts(text: str) -> str:

    replacements = {

        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "â€“": "-",
        "â€”": "-",
        "â€¦": "...",
        "Â ": " ",
        "Â": "",
        "â„¢": " trademark",
        "âœ“": " completed",
        "âœ”": " completed",
        "âœ—": " failed",
        "ðŸ˜Š": " That sounds nice. ",
        "ðŸ˜„": " That sounds great. ",
        "ðŸ‘": " Sounds good. ",
        "ðŸ‘": " Well done. ",
        "ðŸŽ‰": " That's great news. ",
        "ðŸ’¡": " Here's an idea. ",
        "ðŸ”¥": " That's impressive. ",
        "ðŸ”’": " Secure. ",
        "ï¸": "",
    }

    for source, replacement in replacements.items():

        text = text.replace(
            source,
            replacement,
        )

    return text


# =========================================================
# MAIN CLEANER
# =========================================================

def clean_for_speech(
    text: str,
    max_length: int = 6000,
) -> str:
    """
    Convert an LLM response into speech-friendly text.

    The returned text is intended ONLY for TTS.

    The original response must still be used by the UI.
    """

    if not text:

        return ""

    text = str(text)

    text = _fix_encoding_artifacts(
        text
    )

    text = _normalize_unicode(
        text
    )

    text = _replace_emojis(
        text
    )

    text = _remove_remaining_symbols(
        text
    )

    text = _remove_code_blocks(
        text
    )

    text = _clean_links(
        text
    )

    text = _convert_tables(
        text
    )

    text = _clean_headings(
        text
    )

    text = _clean_emphasis(
        text
    )

    text = _clean_inline_code(
        text
    )

    text = _remove_horizontal_rules(
        text
    )

    text = _clean_bullets(
        text
    )

    text = _clean_markdown_characters(
        text
    )

    text = _normalize_punctuation(
        text
    )

    # Remove empty decorative lines.
    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:

            lines.append(line)

    text = " ".join(lines)

    text = _normalize_punctuation(
        text
    )

    # Protect TTS from excessively long responses.
    if len(text) > max_length:

        text = (
            text[:max_length]
            .rsplit(" ", 1)[0]
            .strip()
        )

        text += "."

    return text


# =========================================================
# COMPATIBILITY ALIAS
# =========================================================

def prepare_tts_text(
    text: str,
) -> str:

    return clean_for_speech(
        text
    )