from .actions import SystemActions


class SystemService:
    """
    System capability service.
    """

    def __init__(self):

        self.system = SystemActions()

        self.actions = {
            "battery": self.battery,
            "system_info": self.system_info,
            "current_time": self.current_time,
            "clipboard_get": self.clipboard_get,
            "clipboard_set": self.clipboard_set,
            "list_processes": self.list_processes,
            "shutdown": self.shutdown,
            "restart": self.restart,
            "lock": self.lock,
            "sleep": self.sleep,
            "get_brightness": self.get_brightness,
            "set_brightness": self.set_brightness,
            "get_volume": self.get_volume,
            "set_volume": self.set_volume,
            "mute": self.mute,
            "unmute": self.unmute,
        }

    def execute(self, action, parameters):

        handler = self.actions.get(action)

        if handler is None:
            raise Exception(f"Unsupported system action: {action}")

        return handler(parameters)

    def battery(self, parameters):
        return self.system.battery()

    def system_info(self, parameters):
        return self.system.system_info()

    def current_time(self, parameters):
        return self.system.current_time()

    def clipboard_get(self, parameters):
        return self.system.clipboard_get()

    def clipboard_set(self, parameters):
        return self.system.clipboard_set(
            parameters["text"]
        )

    def list_processes(self, parameters):
        return self.system.list_processes()

    def shutdown(self, parameters):
        return self.system.shutdown()

    def restart(self, parameters):
        return self.system.restart()

    def lock(self, parameters):
        return self.system.lock()

    def sleep(self, parameters):
        return self.system.sleep()

    def get_brightness(self, parameters):
        return self.system.get_brightness()

    def set_brightness(self, parameters):
        return self.system.set_brightness(
            parameters["value"]
        )

    def get_volume(self, parameters):
        return self.system.get_volume()

    def set_volume(self, parameters):
        return self.system.set_volume(
            parameters["value"]
        )

    def mute(self, parameters):
        return self.system.mute()

    def unmute(self, parameters):
        return self.system.unmute()