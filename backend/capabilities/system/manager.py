import datetime
import os
import platform
import subprocess

import psutil
import pyperclip
import screen_brightness_control as sbc

from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import (
    AudioUtilities,
    IAudioEndpointVolume,
)


class SystemManager:

    def battery(self):

        battery = psutil.sensors_battery()

        if battery is None:
            return {
                "available": False
            }

        return {
            "available": True,
            "percent": battery.percent,
            "charging": battery.power_plugged,
        }

    def system_info(self):

        return {
            "os": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    def current_time(self):

        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def clipboard_get(self):

        return pyperclip.paste()

    def clipboard_set(self, text):

        pyperclip.copy(text)

        return "Clipboard updated."

    def list_processes(self):

        processes = []

        for proc in psutil.process_iter(["pid", "name"]):
            processes.append(proc.info)

        return processes

    def shutdown(self):

        os.system("shutdown /s /t 0")

        return "Shutting down."

    def restart(self):

        os.system("shutdown /r /t 0")

        return "Restarting."

    def lock(self):

        os.system("rundll32.exe user32.dll,LockWorkStation")

        return "Computer locked."

    def sleep(self):

        subprocess.run(
            [
                "rundll32.exe",
                "powrprof.dll,SetSuspendState",
                "0,1,0",
            ]
        )

        return "Computer sleeping."

    def get_brightness(self):

        return sbc.get_brightness()[0]

    def set_brightness(self, value):

        sbc.set_brightness(value)

        return f"Brightness set to {value}%"

    def _volume(self):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None,
        )

        return cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

    def get_volume(self):

        volume = self._volume()

        level = volume.GetMasterVolumeLevelScalar()

        return round(level * 100)

    def set_volume(self, value):

        value = max(0, min(100, int(value)))

        volume = self._volume()

        volume.SetMasterVolumeLevelScalar(
            value / 100,
            None
        )

        return f"Volume set to {value}%"

    def mute(self):

        self._volume().SetMute(1, None)

        return "Muted."

    def unmute(self):

        self._volume().SetMute(0, None)

        return "Unmuted."