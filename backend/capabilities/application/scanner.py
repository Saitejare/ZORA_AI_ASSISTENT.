from pathlib import Path
import os


class ApplicationScanner:

    def __init__(self):

        self.paths = [
            Path(os.getenv("ProgramData")) /
            "Microsoft/Windows/Start Menu/Programs",

            Path(os.getenv("APPDATA")) /
            "Microsoft/Windows/Start Menu/Programs"
        ]

    def scan(self):

        apps = {}

        for root in self.paths:

            if not root.exists():
                continue

            for shortcut in root.rglob("*.lnk"):

                name = shortcut.stem.lower()

                apps[name] = str(shortcut)

        return apps