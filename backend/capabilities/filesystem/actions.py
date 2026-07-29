from .manager import FileSystemManager


class FileSystemActions:

    def __init__(self):
        self.manager = FileSystemManager()

    def create_file(self, path):
        return self.manager.create_file(path)

    def delete_file(self, path):
        return self.manager.delete_file(path)

    def rename_file(self, source, destination):
        return self.manager.rename_file(source, destination)

    def move_file(self, source, destination):
        return self.manager.move_file(source, destination)

    def copy_file(self, source, destination):
        return self.manager.copy_file(source, destination)

    def read_file(self, path):
        return self.manager.read_file(path)

    def write_file(self, path, content):
        return self.manager.write_file(path, content)

    def append_file(self, path, content):
        return self.manager.append_file(path, content)

    def create_folder(self, path):
        return self.manager.create_folder(path)

    def delete_folder(self, path):
        return self.manager.delete_folder(path)

    def list_folder(self, path):
        return self.manager.list_folder(path)

    def search_file(self, root, filename):
        return self.manager.search_file(root, filename)