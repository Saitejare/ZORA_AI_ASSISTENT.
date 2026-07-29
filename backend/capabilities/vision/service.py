from .actions import VisionActions


class VisionService:
    """
    Vision capability service.
    """

    def __init__(self):

        self.vision = VisionActions()

        self.actions = {
            "screenshot": self.screenshot,
            "read_text": self.read_text,
            "image_size": self.image_size,
            "image_info": self.image_info,
            "find_template": self.find_template,
            "grayscale": self.grayscale,
        }

    def execute(self, action, parameters):

        handler = self.actions.get(action)

        if handler is None:
            raise Exception(f"Unsupported vision action: {action}")

        return handler(parameters)

    def screenshot(self, parameters):

        return self.vision.screenshot(
            parameters["path"]
        )

    def read_text(self, parameters):

        return self.vision.read_text(
            parameters["image_path"]
        )

    def image_size(self, parameters):

        return self.vision.image_size(
            parameters["image_path"]
        )

    def image_info(self, parameters):

        return self.vision.image_info(
            parameters["image_path"]
        )

    def find_template(self, parameters):

        return self.vision.find_template(
            parameters["image_path"],
            parameters["template_path"],
            parameters.get("threshold", 0.8),
        )

    def grayscale(self, parameters):

        return self.vision.grayscale(
            parameters["image_path"],
            parameters["output_path"],
        )