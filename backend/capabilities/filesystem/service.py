from .actions import FileSystemActions


class FileSystemService:
    """
    Filesystem capability service.
    """

    def __init__(self):

        self.filesystem = FileSystemActions()

        self.actions = {
            "create_file": self.create_file,
            "delete_file": self.delete_file,
            "rename_file": self.rename_file,
            "move_file": self.move_file,
            "copy_file": self.copy_file,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "append_file": self.append_file,
            "create_folder": self.create_folder,
            "delete_folder": self.delete_folder,
            "list_folder": self.list_folder,
            "search_file": self.search_file,
        }

    def execute(self, action, parameters):

        handler = self.actions.get(action)

        if handler is None:
            raise Exception(f"Unsupported filesystem action: {action}")

        return handler(parameters)

    # -------------------------------------------------

    def create_file(self, parameters):

        return self.filesystem.create_file(
            parameters["path"]
        )

    def delete_file(self, parameters):

        return self.filesystem.delete_file(
            parameters["path"]
        )

    def rename_file(self, parameters):

        return self.filesystem.rename_file(
            parameters["source"],
            parameters["destination"],
        )

    def move_file(self, parameters):

        return self.filesystem.move_file(
            parameters["source"],
            parameters["destination"],
        )

    def copy_file(self, parameters):

        return self.filesystem.copy_file(
            parameters["source"],
            parameters["destination"],
        )

    def read_file(self, parameters):

        return self.filesystem.read_file(
            parameters["path"]
        )

    def write_file(self, parameters):

        return self.filesystem.write_file(
            parameters["path"],
            parameters["content"],
        )

    def append_file(self, parameters):

        return self.filesystem.append_file(
            parameters["path"],
            parameters["content"],
        )

    def create_folder(self, parameters):

        return self.filesystem.create_folder(
            parameters["path"]
        )

    def delete_folder(self, parameters):

        return self.filesystem.delete_folder(
            parameters["path"]
        )

    def list_folder(self, parameters):

        return self.filesystem.list_folder(
            parameters["path"]
        )

    def search_file(self, parameters):

        return self.filesystem.search_file(
            parameters["root"],
            parameters["filename"],
        )