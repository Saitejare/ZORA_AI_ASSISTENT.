from rapidfuzz import process, fuzz


class ApplicationMatcher:

    def __init__(self):
        self.threshold = 80

    def match(self, target: str, applications: dict):

        target = target.lower().strip()

        if not target:
            return None

        # =====================================================
        # EXACT MATCH
        # =====================================================

        for name in applications.keys():

            if name.lower().strip() == target:

                return {
                    "name": name,
                    "path": applications[name],
                    "score": 100,
                }

        # =====================================================
        # COMMON WINDOWS APPLICATION ALIASES
        # =====================================================

        aliases = {
            "notepad": [
                "notepad",
                "notepad.exe",
            ],

            "calculator": [
                "calculator",
                "calculator.exe",
                "calc",
                "calc.exe",
                "windows calculator",
            ],

            "paint": [
                "paint",
                "mspaint",
                "mspaint.exe",
                "microsoft paint",
            ],

            "chrome": [
                "chrome",
                "google chrome",
                "chrome.exe",
            ],

            "edge": [
                "edge",
                "microsoft edge",
                "msedge",
                "msedge.exe",
            ],

            "firefox": [
                "firefox",
                "mozilla firefox",
                "firefox.exe",
            ],

            "vscode": [
                "vscode",
                "vs code",
                "visual studio code",
                "code",
                "code.exe",
            ],

            "cmd": [
                "cmd",
                "command prompt",
                "cmd.exe",
            ],

            "powershell": [
                "powershell",
                "windows powershell",
                "powershell.exe",
            ],

            "word": [
                "word",
                "microsoft word",
                "winword",
                "winword.exe",
            ],

            "excel": [
                "excel",
                "microsoft excel",
                "excel.exe",
            ],

            "powerpoint": [
                "powerpoint",
                "microsoft powerpoint",
                "powerpnt",
                "powerpnt.exe",
            ],
        }

        # =====================================================
        # ALIAS MATCH
        # =====================================================

        target_aliases = aliases.get(
            target,
            [target],
        )

        for alias in target_aliases:

            for name in applications.keys():

                if name.lower().strip() == alias:

                    return {
                        "name": name,
                        "path": applications[name],
                        "score": 100,
                    }

        # =====================================================
        # FUZZY MATCH
        # =====================================================

        choices = list(
            applications.keys()
        )

        result = process.extractOne(
            target,
            choices,
            scorer=fuzz.WRatio,
        )

        if result is None:
            return None

        name, score, _ = result

        # Higher threshold prevents unrelated applications
        # such as "Send To OneNote" from matching "notepad".

        if score < self.threshold:
            return None

        return {
            "name": name,
            "path": applications[name],
            "score": score,
        }