from .manager import VisionManager


class VisionActions:

    def __init__(self):
        self.manager = VisionManager()

    def screenshot(self, path):
        return self.manager.screenshot(path)

    def read_text(self, image_path):
        return self.manager.read_text(image_path)

    def image_size(self, image_path):
        return self.manager.image_size(image_path)

    def image_info(self, image_path):
        return self.manager.image_info(image_path)

    def find_template(
        self,
        image_path,
        template_path,
        threshold=0.8,
    ):
        return self.manager.find_template(
            image_path,
            template_path,
            threshold,
        )

    def grayscale(
        self,
        image_path,
        output_path,
    ):
        return self.manager.grayscale(
            image_path,
            output_path,
        )