from .manager import SystemManager


class SystemActions:

    def __init__(self):
        self.manager = SystemManager()

    def battery(self):
        return self.manager.battery()

    def system_info(self):
        return self.manager.system_info()

    def current_time(self):
        return self.manager.current_time()

    def clipboard_get(self):
        return self.manager.clipboard_get()

    def clipboard_set(self, text):
        return self.manager.clipboard_set(text)

    def list_processes(self):
        return self.manager.list_processes()

    def shutdown(self):
        return self.manager.shutdown()

    def restart(self):
        return self.manager.restart()

    def lock(self):
        return self.manager.lock()

    def sleep(self):
        return self.manager.sleep()

    def get_brightness(self):
        return self.manager.get_brightness()

    def set_brightness(self, value):
        return self.manager.set_brightness(value)

    def get_volume(self):
        return self.manager.get_volume()

    def set_volume(self, value):
        return self.manager.set_volume(value)

    def mute(self):
        return self.manager.mute()

    def unmute(self):
        return self.manager.unmute()