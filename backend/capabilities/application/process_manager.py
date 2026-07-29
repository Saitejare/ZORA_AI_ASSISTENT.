import psutil


class ProcessManager:

    def list_running(self):
        processes = []

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                info = proc.info
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return processes

    def is_running(self, app_name: str):

        app_name = app_name.lower()

        for proc in psutil.process_iter(["name"]):
            try:
                name = proc.info["name"]

                if name and app_name in name.lower():
                    return True

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return False

    def terminate(self, app_name: str):

        app_name = app_name.lower()

        count = 0

        for proc in psutil.process_iter(["name"]):

            try:
                name = proc.info["name"]

                if name and app_name in name.lower():
                    proc.terminate()
                    count += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return count