from __future__ import annotations

import logging
import re

from backend.llm.service import LLMService
from backend.planner.parser import PlanParser
from backend.planner.models import (
    ExecutionPlan,
    PlanStep,
)


logger = logging.getLogger(__name__)


PLANNER_PROMPT = """
You are ZORA's execution planner.

Your job is to convert a user's COMPUTER ACTION request
into a valid multi-step execution plan.

Return ONLY valid JSON.

Never explain.

Never use Markdown.

Never return anything outside JSON.

========================================================
JSON FORMAT
========================================================

{
    "steps": [
        {
            "capability": "application",
            "action": "launch",
            "parameters": {
                "target": "notepad"
            }
        }
    ]
}

========================================================
AVAILABLE CAPABILITIES
========================================================

application

launch(target)
terminate(target)
activate(target)
minimize(target)
maximize(target)
close_window(target)

--------------------------------------------------------

browser

open_url(url)
search(query)
new_tab()
list_tabs()
switch_tab(index)
close_tab()
title()
metadata()
text()
close()

--------------------------------------------------------

filesystem

create_file(path)
delete_file(path)
rename_file(source,destination)
move_file(source,destination)
copy_file(source,destination)
read_file(path)
write_file(path,content)
append_file(path,content)
create_folder(path)
delete_folder(path)
list_folder(path)
search_file(root,filename)

--------------------------------------------------------

desktop

move_mouse(x,y)
click()
double_click()
right_click()
scroll(amount)
type_text(text)
press_key(key)
hotkey(keys)
drag(x,y)
screenshot(path)
wait(seconds)
position()
screen_size()

--------------------------------------------------------

system

battery()
system_info()
current_time()
date()
clipboard_get()
clipboard_set(text)
list_processes()
shutdown()
restart()
lock()
sleep()
get_brightness()
set_brightness(value)
get_volume()
set_volume(value)
mute()
unmute()

--------------------------------------------------------

vision

screenshot(path)
read_text(image_path)
image_size(image_path)
image_info(image_path)
find_template(image_path,template_path)
grayscale(image_path,output_path)

========================================================
IMPORTANT PLANNING RULES
========================================================

1. You MAY generate multiple steps.

2. Each step must contain exactly ONE action.

3. Execute the requested actions in the correct order.

4. Do NOT stop after the first action.

5. If an application must be opened before typing,
   launch the application first.

6. When an application is launched and another action
   immediately depends on its window, insert:

   desktop/wait

   with approximately 1 second.

7. Never invent a capability.

8. Never invent an action.

9. Never invent parameter names.

10. Never invent file paths.

11. Never invent URLs.

12. Use "desktop/type_text" for typing into the
    currently active application.

13. Use "desktop/press_key" for keyboard keys.

14. Use "desktop/hotkey" for keyboard combinations.

15. Use "application/launch" for Windows applications.

16. Use "browser/open_url" for websites.

========================================================
WINDOWS APPLICATIONS
========================================================

The following are desktop applications:

chrome
edge
firefox
vscode
visual studio
cmd
powershell
notepad
calculator
paint
excel
word
powerpoint

Use:

capability = application
action = launch

========================================================
WEBSITES
========================================================

The following are websites:

google
youtube
amazon
flipkart
github
linkedin
instagram
facebook
gmail
chatgpt
openai
spotify
netflix
leetcode
hackerrank
codeforces
geeksforgeeks
lendi

Use:

capability = browser
action = open_url

========================================================
EXAMPLE 1
========================================================

User:

Open Notepad

Return:

{
    "steps": [
        {
            "capability": "application",
            "action": "launch",
            "parameters": {
                "target": "notepad"
            }
        }
    ]
}

========================================================
EXAMPLE 2
========================================================

User:

Open Notepad and write Hello World

Return:

{
    "steps": [
        {
            "capability": "application",
            "action": "launch",
            "parameters": {
                "target": "notepad"
            }
        },
        {
            "capability": "desktop",
            "action": "wait",
            "parameters": {
                "seconds": 1
            }
        },
        {
            "capability": "desktop",
            "action": "type_text",
            "parameters": {
                "text": "Hello World"
            }
        }
    ]
}

========================================================
EXAMPLE 3
========================================================

User:

Launch Calculator

Return:

{
    "steps": [
        {
            "capability": "application",
            "action": "launch",
            "parameters": {
                "target": "calculator"
            }
        }
    ]
}

========================================================
EXAMPLE 4
========================================================

User:

Open Chrome and search Python programming

Return:

{
    "steps": [
        {
            "capability": "application",
            "action": "launch",
            "parameters": {
                "target": "chrome"
            }
        },
        {
            "capability": "desktop",
            "action": "wait",
            "parameters": {
                "seconds": 2
            }
        },
        {
            "capability": "browser",
            "action": "search",
            "parameters": {
                "query": "Python programming"
            }
        }
    ]
}

========================================================
EXAMPLE 5
========================================================

User:

Open Notepad, type Hello ZORA, then press Enter

Return:

{
    "steps": [
        {
            "capability": "application",
            "action": "launch",
            "parameters": {
                "target": "notepad"
            }
        },
        {
            "capability": "desktop",
            "action": "wait",
            "parameters": {
                "seconds": 1
            }
        },
        {
            "capability": "desktop",
            "action": "type_text",
            "parameters": {
                "text": "Hello ZORA"
            }
        },
        {
            "capability": "desktop",
            "action": "press_key",
            "parameters": {
                "key": "enter"
            }
        }
    ]
}

========================================================
EXAMPLE 6
========================================================

User:

Create a folder called AI on my Desktop

Return:

{
    "steps": [
        {
            "capability": "filesystem",
            "action": "create_folder",
            "parameters": {
                "path": "Desktop/AI"
            }
        }
    ]
}

========================================================
EXAMPLE 7
========================================================

User:

Take a screenshot

Return:

{
    "steps": [
        {
            "capability": "desktop",
            "action": "screenshot",
            "parameters": {
                "path": "Desktop/screenshot.png"
            }
        }
    ]
}

========================================================
EXAMPLE 8
========================================================

User:

Open YouTube

Return:

{
    "steps": [
        {
            "capability": "browser",
            "action": "open_url",
            "parameters": {
                "url": "youtube"
            }
        }
    ]
}

========================================================

Always return valid JSON.

Never return explanations.

Never return Markdown.
"""


class Planner:

    def __init__(self):

        self.llm = LLMService()

        self.parser = PlanParser()

    # =====================================================
    # DETERMINISTIC DESKTOP SHORTCUTS
    # =====================================================

    def _desktop_shortcut(
        self,
        user_input: str,
    ) -> ExecutionPlan | None:

        text = re.sub(
            r"\s+",
            " ",
            user_input.strip(),
        )

        normalized = text.lower()

        # =================================================
        # OPEN NOTEPAD + WRITE
        # =================================================

        match = re.match(
            r"^(?:open|launch|start)\s+notepad"
            r"(?:\s+and\s+|\s*,\s*)"
            r"(?:write|type)\s+(.+)$",
            text,
            re.IGNORECASE,
        )

        if match:

            content = match.group(1).strip()

            return ExecutionPlan(
                steps=[
                    PlanStep(
                        capability="application",
                        action="launch",
                        parameters={
                            "target": "notepad",
                        },
                    ),
                    PlanStep(
                        capability="desktop",
                        action="wait",
                        parameters={
                            "seconds": 1,
                        },
                    ),
                    PlanStep(
                        capability="desktop",
                        action="type_text",
                        parameters={
                            "text": content,
                        },
                    ),
                ]
            )

        # =================================================
        # OPEN CALCULATOR
        # =================================================

        if normalized in {
            "open calculator",
            "launch calculator",
            "start calculator",
        }:

            return ExecutionPlan(
                steps=[
                    PlanStep(
                        capability="application",
                        action="launch",
                        parameters={
                            "target": "calculator",
                        },
                    )
                ]
            )

        # =================================================
        # OPEN NOTEPAD
        # =================================================

        if normalized in {
            "open notepad",
            "launch notepad",
            "start notepad",
        }:

            return ExecutionPlan(
                steps=[
                    PlanStep(
                        capability="application",
                        action="launch",
                        parameters={
                            "target": "notepad",
                        },
                    )
                ]
            )

        # =================================================
        # TYPE TEXT
        # =================================================

        match = re.match(
            r"^(?:type|write)\s+(.+)$",
            text,
            re.IGNORECASE,
        )

        if match:

            content = match.group(1).strip()

            if content:

                return ExecutionPlan(
                    steps=[
                        PlanStep(
                            capability="desktop",
                            action="type_text",
                            parameters={
                                "text": content,
                            },
                        )
                    ]
                )

        # =================================================
        # PRESS KEY
        # =================================================

        match = re.match(
            r"^press\s+(.+)$",
            text,
            re.IGNORECASE,
        )

        if match:

            key = match.group(1).strip().lower()

            return ExecutionPlan(
                steps=[
                    PlanStep(
                        capability="desktop",
                        action="press_key",
                        parameters={
                            "key": key,
                        },
                    )
                ]
            )

        # =================================================
        # TAKE SCREENSHOT
        # =================================================

        if normalized in {
            "take a screenshot",
            "take screenshot",
            "screenshot",
            "capture screenshot",
        }:

            return ExecutionPlan(
                steps=[
                    PlanStep(
                        capability="desktop",
                        action="screenshot",
                        parameters={
                            "path": "Desktop/screenshot.png",
                        },
                    )
                ]
            )

        return None

    # =====================================================
    # BROWSER SHORTCUTS
    # =====================================================

    def _browser_shortcut(
        self,
        user_input: str,
    ) -> ExecutionPlan | None:

        normalized = re.sub(
            r"\s+",
            " ",
            user_input.strip().lower(),
        )

        # =================================================
        # YOUTUBE SEARCH
        # =================================================

        youtube_patterns = [

            r"^(?:open\s+)?youtube\s+"
            r"(?:and\s+)?search(?:\s+for)?\s+(.+)$",

            r"^search\s+youtube\s+for\s+(.+)$",

            r"^play\s+(.+?)\s+on\s+youtube$",

            r"^open\s+youtube\s+and\s+search\s+(.+)$",
        ]

        for pattern in youtube_patterns:

            match = re.match(
                pattern,
                normalized,
                re.IGNORECASE,
            )

            if match:

                query = match.group(1).strip()

                if query:

                    return ExecutionPlan(
                        steps=[
                            PlanStep(
                                capability="browser",
                                action="search",
                                parameters={
                                    "query": query,
                                    "engine": "youtube",
                                },
                            )
                        ]
                    )

        # =================================================
        # OPEN YOUTUBE
        # =================================================

        if normalized in {
            "open youtube",
            "open you tube",
            "youtube",
            "open youtube.com",
            "open www.youtube.com",
        }:

            return ExecutionPlan(
                steps=[
                    PlanStep(
                        capability="browser",
                        action="open_url",
                        parameters={
                            "url": "youtube",
                        },
                    )
                ]
            )

        # =================================================
        # OPEN URL
        # =================================================

        url_match = re.match(
            r"^open\s+"
            r"((?:https?://)?"
            r"(?:www\.)?"
            r"[a-z0-9-]+\."
            r"[a-z]{2,}"
            r"(?:/\S*)?)$",
            normalized,
            re.IGNORECASE,
        )

        if url_match:

            return ExecutionPlan(
                steps=[
                    PlanStep(
                        capability="browser",
                        action="open_url",
                        parameters={
                            "url": url_match.group(1),
                        },
                    )
                ]
            )

        return None

    # =====================================================
    # CREATE PLAN
    # =====================================================

    def create_plan(
        self,
        user_input: str,
        memory_context: str = "",
    ) -> ExecutionPlan:

        # -------------------------------------------------
        # Desktop deterministic commands
        # -------------------------------------------------

        desktop_shortcut = self._desktop_shortcut(
            user_input
        )

        if desktop_shortcut is not None:

            logger.info(
                "Planner used deterministic desktop shortcut"
            )

            return desktop_shortcut

        # -------------------------------------------------
        # Browser deterministic commands
        # -------------------------------------------------

        browser_shortcut = self._browser_shortcut(
            user_input
        )

        if browser_shortcut is not None:

            logger.info(
                "Planner used deterministic browser shortcut"
            )

            return browser_shortcut

        # -------------------------------------------------
        # LLM planner
        # -------------------------------------------------

        prompt = PLANNER_PROMPT

        if memory_context:

            prompt += (
                "\n\nRelevant User Memory:\n"
                + memory_context
            )

        prompt += (
            "\n\nUser Request:\n"
            + user_input
        )

        response = self.llm.one_shot(
            prompt
        )

        logger.info(
            "Planner generated plan response"
        )

        return self.parser.parse(
            response
        )