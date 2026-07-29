from .actions import DesktopActions


class DesktopService:
    """
    Desktop automation capability.
    """

    def __init__(self):

        self.desktop = DesktopActions()

        self.actions = {
            "move_mouse": self.move_mouse,
            "click": self.click,
            "double_click": self.double_click,
            "right_click": self.right_click,
            "scroll": self.scroll,
            "type_text": self.type_text,
            "press_key": self.press_key,
            "hotkey": self.hotkey,
            "drag": self.drag,
            "screenshot": self.screenshot,
            "wait": self.wait,
            "position": self.position,
            "screen_size": self.screen_size,
        }

    def execute(self, action, parameters):

        handler = self.actions.get(action)

        if handler is None:
            raise Exception(f"Unsupported desktop action: {action}")

        return handler(parameters)

    def move_mouse(self, parameters):

        return self.desktop.move_mouse(
            parameters["x"],
            parameters["y"],
        )

    def click(self, parameters):

        return self.desktop.click(
            parameters.get("x"),
            parameters.get("y"),
        )

    def double_click(self, parameters):

        return self.desktop.double_click(
            parameters.get("x"),
            parameters.get("y"),
        )

    def right_click(self, parameters):

        return self.desktop.right_click(
            parameters.get("x"),
            parameters.get("y"),
        )

    def scroll(self, parameters):

        return self.desktop.scroll(
            parameters["amount"]
        )

    def type_text(self, parameters):

        return self.desktop.type_text(
            parameters["text"]
        )

    def press_key(self, parameters):

        return self.desktop.press_key(
            parameters["key"]
        )

    def hotkey(self, parameters):

        return self.desktop.hotkey(
            parameters["keys"]
        )

    def drag(self, parameters):

        return self.desktop.drag(
            parameters["x"],
            parameters["y"],
        )

    def screenshot(self, parameters):

        return self.desktop.screenshot(
            parameters["path"]
        )

    def wait(self, parameters):

        return self.desktop.wait(
            parameters["seconds"]
        )

    def position(self, parameters):

        return self.desktop.position()

    def screen_size(self, parameters):

        return self.desktop.screen_size()