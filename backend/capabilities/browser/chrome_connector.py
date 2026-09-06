import requests
import subprocess
import time


class ChromeConnector:

    DEBUG_PORT = 9222

    def start_debugging(self):

        try:

            requests.get(
                f"http://127.0.0.1:{self.DEBUG_PORT}/json/version",
                timeout=1,
            )

            return

        except Exception:
            pass

        subprocess.Popen(
            [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                f"--remote-debugging-port={self.DEBUG_PORT}",
            ]
        )

        time.sleep(3)