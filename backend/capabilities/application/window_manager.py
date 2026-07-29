import pygetwindow as gw


class WindowManager:

    def get_windows(self):

        windows = []

        for window in gw.getAllWindows():

            if window.title.strip():

                windows.append({
                    "title": window.title,
                    "window": window
                })

        return windows

    def find_window(self, app_name: str):

        app_name = app_name.lower()

        for window in gw.getAllWindows():

            try:
                if app_name in window.title.lower():
                    return window
            except Exception:
                continue

        return None

    def activate(self, app_name: str):

        window = self.find_window(app_name)

        if window is None:
            return False

        window.activate()

        return True

    def minimize(self, app_name: str):

        window = self.find_window(app_name)

        if window is None:
            return False

        window.minimize()

        return True

    def maximize(self, app_name: str):

        window = self.find_window(app_name)

        if window is None:
            return False

        window.maximize()

        return True

    def close(self, app_name: str):

        window = self.find_window(app_name)

        if window is None:
            return False

        window.close()

        return True