from __future__ import annotations

import logging
import re

from backend.planner.planner import Planner
from backend.planner.executor import PlanExecutor

from backend.agent.conversation_manager import ConversationManager
from backend.memory.service import MemoryService
from backend.llm.service import LLMService


logger = logging.getLogger(__name__)


class Orchestrator:

    def __init__(
        self,
        planner=None,
        executor=None,
        conversation=None,
        memory=None,
        llm=None,
    ) -> None:

        self.planner = planner or Planner()

        self.executor = (
            executor
            or PlanExecutor()
        )

        self.conversation = (
            conversation
            or ConversationManager()
        )

        self.memory = (
            memory
            or MemoryService()
        )

        self.llm = llm or LLMService()

    # =====================================================
    # RESPONSE CLEANING
    # =====================================================

    @staticmethod
    def _clean_response(text: str) -> str:
        """
        Clean assistant output before displaying or speaking.

        Removes:
        - HTML tags
        - vertical bars
        - markdown separators
        - markdown bullets
        - markdown emphasis
        - backticks
        - excessive punctuation
        """

        if not text:
            return ""

        text = str(text)

        # -------------------------------------------------
        # HTML
        # -------------------------------------------------

        text = re.sub(
            r"<br\s*/?>",
            "\n",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"<[^>]+>",
            "",
            text,
        )

        # -------------------------------------------------
        # Markdown bold / italic
        # -------------------------------------------------

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
            r"(?<!\w)\*(.*?)\*(?!\w)",
            r"\1",
            text,
            flags=re.DOTALL,
        )

        # -------------------------------------------------
        # Markdown headings
        # -------------------------------------------------

        text = re.sub(
            r"^\s*#{1,6}\s*",
            "",
            text,
            flags=re.MULTILINE,
        )

        # -------------------------------------------------
        # Vertical bars
        # -------------------------------------------------

        text = text.replace(
            "||",
            ". ",
        )

        text = text.replace(
            "|",
            " ",
        )

        # -------------------------------------------------
        # Markdown horizontal separators
        # -------------------------------------------------

        text = re.sub(
            r"^\s*[-*_]{3,}\s*$",
            "",
            text,
            flags=re.MULTILINE,
        )

        # -------------------------------------------------
        # Markdown bullet markers
        # -------------------------------------------------

        text = re.sub(
            r"^\s*[-*+]\s+",
            "",
            text,
            flags=re.MULTILINE,
        )

        # -------------------------------------------------
        # Backticks
        # -------------------------------------------------

        text = text.replace(
            "`",
            "",
        )

        # -------------------------------------------------
        # Excessive underscores
        # -------------------------------------------------

        text = re.sub(
            r"_+",
            " ",
            text,
        )

        # -------------------------------------------------
        # Normalize spaces
        # -------------------------------------------------

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        # -------------------------------------------------
        # Normalize blank lines
        # -------------------------------------------------

        text = re.sub(
            r"\n\s*\n\s*\n+",
            "\n\n",
            text,
        )

        # -------------------------------------------------
        # Remove spaces before punctuation
        # -------------------------------------------------

        text = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            text,
        )

        # -------------------------------------------------
        # Repeated punctuation
        # -------------------------------------------------

        text = re.sub(
            r"\.{3,}",
            "...",
            text,
        )

        text = re.sub(
            r"!{2,}",
            "!",
            text,
        )

        text = re.sub(
            r"\?{2,}",
            "?",
            text,
        )

        return text.strip()

    # =====================================================
    # MAIN REQUEST PIPELINE
    # =====================================================

    def run(
        self,
        user_input: str,
    ) -> str:

        user_input = user_input.strip()

        if not user_input:
            raise ValueError(
                "User input cannot be empty."
            )

        logger.info(
            "Processing request: %s",
            user_input,
        )

        # =================================================
        # MEMORY
        # =================================================

        try:

            memories = self.memory.recall(
                user_input
            )

        except Exception:

            logger.exception(
                "Memory recall failed."
            )

            memories = []

        # =================================================
        # STORE USER MESSAGE
        # =================================================

        try:

            self.conversation.add_user_message(
                user_input,
                memories,
            )

        except Exception:

            logger.exception(
                "Failed to store user message."
            )

        # =================================================
        # BUILD MEMORY CONTEXT
        # =================================================

        memory_context = "\n".join(
            item.get("text", "")
            for item in memories
            if isinstance(item, dict)
        )

        # =================================================
        # COMMAND DETECTION
        # =================================================

        try:

            if self.is_command(user_input):

                logger.info(
                    "Request classified as command."
                )

                return self._run_command(
                    user_input,
                    memory_context,
                )

        except Exception:

            logger.exception(
                "Command classification failed."
            )

        # =================================================
        # CONVERSATION
        # =================================================

        try:

            logger.info(
                "Request classified as conversation."
            )

            final_response = self.llm.chat(
                user_input,
                memory_context,
            )

            final_response = self._clean_response(
                final_response
            )

            if not final_response:

                final_response = (
                    "I'm here. "
                    "How can I help you?"
                )

            logger.info(
                "Assistant response: %s",
                final_response,
            )

            try:

                self.conversation.add_assistant_message(
                    final_response
                )

            except Exception:

                logger.exception(
                    "Failed to store assistant response."
                )

            try:

                self.memory.remember(
                    user_input
                )

            except Exception:

                logger.exception(
                    "Memory storage failed."
                )

            logger.info(
                "Request completed."
            )

            return final_response

        except Exception:

            logger.exception(
                "Conversation processing failed."
            )

            raise

    # =====================================================
    # COMMAND PIPELINE
    # =====================================================

    def _run_command(
        self,
        user_input: str,
        memory_context: str,
    ) -> str:

        logger.info(
            "Creating execution plan for: %s",
            user_input,
        )

        plan = self.planner.create_plan(
            user_input=user_input,
            memory_context=memory_context,
        )

        logger.info(
            "Planner generated %d step(s)",
            len(plan.steps),
        )

        if plan.empty():

            logger.info(
                "Planner returned an empty plan."
            )

            return (
                "I couldn't determine the action "
                "you want me to perform."
            )

        # =================================================
        # EXECUTE ALL STEPS
        # =================================================

        responses = self.executor.execute(
            plan,
            user_input,
        )

        # =================================================
        # BUILD RESPONSE
        # =================================================

        if responses:

            final_response = "\n".join(
                str(response)
                for response in responses
                if response is not None
                and str(response).strip()
            ).strip()

        else:

            final_response = ""

        final_response = self._clean_response(
            final_response
        )

        if not final_response:

            final_response = (
                "The requested action has been completed."
            )

        logger.info(
            "Assistant response: %s",
            final_response,
        )

        # =================================================
        # STORE ASSISTANT RESPONSE
        # =================================================

        try:

            self.conversation.add_assistant_message(
                final_response
            )

        except Exception:

            logger.exception(
                "Failed to store assistant response."
            )

        # =================================================
        # STORE MEMORY
        # =================================================

        try:

            self.memory.remember(
                user_input
            )

        except Exception:

            logger.exception(
                "Memory storage failed."
            )

        logger.info(
            "Request completed."
        )

        return final_response

    # =====================================================
    # COMMAND / CONVERSATION CLASSIFICATION
    # =====================================================

    def is_command(
        self,
        user_input: str,
    ) -> bool:
        """
        Determine whether the request should be executed
        as a real desktop/system/browser command.

        Deterministic rules are checked first so common
        Windows actions do not get accidentally classified
        as conversation.
        """

        text = user_input.strip().lower()

        # =================================================
        # DIRECT COMMAND KEYWORDS
        # =================================================

        command_patterns = [

            # Applications
            r"\bopen\s+(notepad|calculator|paint|chrome|edge|firefox|vscode|visual studio|cmd|powershell|excel|word|powerpoint)\b",
            r"\blaunch\s+",
            r"\bstart\s+(notepad|calculator|paint|chrome|edge|firefox|vscode|visual studio|cmd|powershell|excel|word|powerpoint)\b",
            r"\bclose\s+(notepad|calculator|paint|chrome|edge|firefox|vscode|visual studio|cmd|powershell|excel|word|powerpoint)\b",
            r"\bterminate\s+",
            r"\bminimize\s+",
            r"\bmaximize\s+",
            r"\bactivate\s+",

            # Desktop
            r"\btype\s+",
            r"\bwrite\s+",
            r"\bclick\b",
            r"\bdouble\s+click\b",
            r"\bright\s+click\b",
            r"\bmove\s+(the\s+)?mouse\b",
            r"\bpress\s+",
            r"\bhotkey\b",
            r"\bscroll\b",
            r"\bdrag\b",
            r"\btake\s+(a\s+)?screenshot\b",
            r"\bscreenshot\b",

            # Filesystem
            r"\bcreate\s+(a\s+)?file\b",
            r"\bcreate\s+(a\s+)?folder\b",
            r"\bmake\s+(a\s+)?folder\b",
            r"\bdelete\s+(the\s+)?file\b",
            r"\bdelete\s+(the\s+)?folder\b",
            r"\brename\s+(the\s+)?file\b",
            r"\bmove\s+(the\s+)?file\b",
            r"\bcopy\s+(the\s+)?file\b",
            r"\bread\s+(the\s+)?file\b",
            r"\bwrite\s+.*\s+(to|into|in)\s+.*\.(txt|py|js|json|md|csv)\b",

            # Browser
            r"\bopen\s+(google|youtube|amazon|flipkart|github|linkedin|instagram|facebook|gmail|chatgpt|openai|spotify|netflix|leetcode|hackerrank|codeforces|geeksforgeeks)\b",
            r"\bsearch\s+(for\s+)?",
            r"\bsearch\s+youtube\b",
            r"\bopen\s+https?://",
            r"\bgo\s+to\s+",

            # System
            r"\bwhat\s+time\s+is\s+it\b",
            r"\bcurrent\s+time\b",
            r"\bbattery\b",
            r"\bsystem\s+info\b",
            r"\bget\s+volume\b",
            r"\bset\s+volume\b",
            r"\bvolume\b",
            r"\bbrightness\b",
            r"\bshutdown\b",
            r"\brestart\b",
            r"\block\s+(the\s+)?computer\b",
            r"\bput\s+(the\s+)?computer\s+to\s+sleep\b",
        ]

        for pattern in command_patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE,
            ):
                return True

        # =================================================
        # IMPORTANT COMBINATION PATTERNS
        # =================================================

        # Examples:
        #
        # "Open Notepad and write Hello"
        # "Launch Chrome and type ..."
        # "Open calculator and ..."
        #
        # If a request starts with an application action
        # and contains another action, it is definitely
        # an executable command.

        if re.search(
            r"^\s*(open|launch|start)\s+.+\s+and\s+"
            r"(write|type|press|click|search|open|create|"
            r"save|close)",
            text,
            re.IGNORECASE,
        ):
            return True

        # =================================================
        # LLM CLASSIFICATION
        # =================================================

        prompt = f"""
Classify the following request as exactly one of:

COMMAND
CONVERSATION

COMMAND means ZORA must actually perform an action
on the user's computer.

Examples of COMMAND:
- Open Notepad
- Launch Calculator
- Open Chrome
- Type Hello World
- Write Hello into Notepad
- Click the mouse
- Take a screenshot
- Create a folder on Desktop
- Delete a file
- Search Google for Python
- Open YouTube
- Set the volume to 50
- Open Notepad and write Hello World
- Launch Chrome and search Python programming

CONVERSATION means the user only wants information,
discussion, explanation, greeting, or a normal answer.

Examples of CONVERSATION:
- Hello
- Good morning
- How are you?
- What is machine learning?
- Explain Java inheritance
- Who created you?
- Tell me about my friend
- What is Python?
- I am learning Java

Important:
If the user asks ZORA to DO something on the computer,
return COMMAND.

User request:
{user_input}

Return ONLY:
COMMAND
or
CONVERSATION
"""

        result = self.llm.generate(
            prompt
        )

        normalized = (
            result
            .strip()
            .upper()
        )

        logger.info(
            "Command classifier result: %s",
            normalized,
        )

        if normalized.startswith("COMMAND"):

            return True

        if normalized.startswith("CONVERSATION"):

            return False

        # Safe fallback:
        return False

    # =====================================================
    # SHUTDOWN
    # =====================================================

    def shutdown(self) -> None:

        logger.info(
            "Shutting down Orchestrator"
        )

        try:

            self.executor.shutdown()

        except Exception:

            logger.exception(
                "Executor shutdown failed."
            )