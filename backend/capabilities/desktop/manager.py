import time

import pyautogui


class DesktopManager:

    def move_mouse(self, x: int, y: int):

        pyautogui.moveTo(x, y, duration=0.2)

        return f"Mouse moved to ({x}, {y})"

    def click(self, x=None, y=None):

        pyautogui.click(x=x, y=y)

        return "Mouse clicked"

    def double_click(self, x=None, y=None):

        pyautogui.doubleClick(x=x, y=y)

        return "Mouse double-clicked"

    def right_click(self, x=None, y=None):

        pyautogui.rightClick(x=x, y=y)

        return "Mouse right-clicked"

    def scroll(self, amount: int):

        pyautogui.scroll(amount)

        return f"Scrolled {amount}"

    def type_text(self, text: str):

        pyautogui.write(text, interval=0.03)

        return f"Typed: {text}"

    def press_key(self, key: str):

        pyautogui.press(key)

        return f"Pressed {key}"

    def hotkey(self, *keys):

        pyautogui.hotkey(*keys)

        return f"Pressed {' + '.join(keys)}"

    def drag(self, x: int, y: int):

        pyautogui.dragTo(x, y, duration=0.5)

        return f"Dragged mouse to ({x}, {y})"

    def screenshot(self, path: str):

        image = pyautogui.screenshot()

        image.save(path)

        return f"Screenshot saved to {path}"

    def wait(self, seconds: float):

        time.sleep(seconds)

        return f"Waited {seconds} seconds"

    def position(self):

        pos = pyautogui.position()

        return {
            "x": pos.x,
            "y": pos.y
        }

    def screen_size(self):

        size = pyautogui.size()

        return {
            "width": size.width,
            "height": size.height
        }