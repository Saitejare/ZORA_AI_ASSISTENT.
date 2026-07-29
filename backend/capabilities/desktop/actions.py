from .manager import DesktopManager


class DesktopActions:

    def __init__(self):
        self.manager = DesktopManager()

    def move_mouse(self, x, y):
        return self.manager.move_mouse(x, y)

    def click(self, x=None, y=None):
        return self.manager.click(x, y)

    def double_click(self, x=None, y=None):
        return self.manager.double_click(x, y)

    def right_click(self, x=None, y=None):
        return self.manager.right_click(x, y)

    def scroll(self, amount):
        return self.manager.scroll(amount)

    def type_text(self, text):
        return self.manager.type_text(text)

    def press_key(self, key):
        return self.manager.press_key(key)

    def hotkey(self, keys):
        return self.manager.hotkey(*keys)

    def drag(self, x, y):
        return self.manager.drag(x, y)

    def screenshot(self, path):
        return self.manager.screenshot(path)

    def wait(self, seconds):
        return self.manager.wait(seconds)

    def position(self):
        return self.manager.position()

    def screen_size(self):
        return self.manager.screen_size()