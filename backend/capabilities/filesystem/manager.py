from pathlib import Path
import shutil
import os

class FileSystemManager:

    def create_file(self, path: str):

        file = Path(path)
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch(exist_ok=True)

        return f"File created: {file}"

    def delete_file(self, path: str):

        file = Path(path)

        if not file.exists():
            raise FileNotFoundError(path)

        file.unlink()

        return f"File deleted: {file}"

    def rename_file(self, source: str, destination: str):

        src = Path(source)

        if not src.exists():
            raise FileNotFoundError(source)

        dst = Path(destination)

        src.rename(dst)

        return f"Renamed to: {dst}"

    def move_file(self, source: str, destination: str):

        src = Path(source)

        if not src.exists():
            raise FileNotFoundError(source)

        dst = Path(destination)

        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(src), str(dst))

        return f"Moved to: {dst}"

    def copy_file(self, source: str, destination: str):

        src = Path(source)

        if not src.exists():
            raise FileNotFoundError(source)

        dst = Path(destination)

        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src, dst)

        return f"Copied to: {dst}"

    def read_file(self, path: str):

        file = Path(path)

        if not file.exists():
            raise FileNotFoundError(path)

        return file.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str):

        file = Path(path)

        file.parent.mkdir(parents=True, exist_ok=True)

        file.write_text(content, encoding="utf-8")

        return f"Written to: {file}"

    def append_file(self, path: str, content: str):

        file = Path(path)

        file.parent.mkdir(parents=True, exist_ok=True)

        with open(file, "a", encoding="utf-8") as f:
            f.write(content)

        return f"Appended to: {file}"

    def create_folder(self, path: str):

        folder = Path(path)

        folder.mkdir(parents=True, exist_ok=True)

        return f"Folder created: {folder}"

    def delete_folder(self, path: str):

        folder = Path(path)

        if not folder.exists():
            raise FileNotFoundError(path)

        shutil.rmtree(folder)

        return f"Folder deleted: {folder}"

    def list_folder(self, path: str):

        folder = Path(path)

        if not folder.exists():
            raise FileNotFoundError(path)

        return [item.name for item in folder.iterdir()]

    def search_file(self, root: str, filename: str):

        root = Path(root)

        if not root.exists():
            raise FileNotFoundError(root)

        matches = []

        for file in root.rglob("*"):

            if file.is_file() and filename.lower() in file.name.lower():
                matches.append(str(file))

        return matches
    def resolve_path(self, path: str):

        desktop = Path.home() / "Desktop"
        documents = Path.home() / "Documents"
        downloads = Path.home() / "Downloads"

        path = path.replace("\\", "/")

        if path.startswith("Desktop/"):
            return desktop / path.replace("Desktop/", "", 1)

        if path.startswith("Documents/"):
            return documents / path.replace("Documents/", "", 1)

        if path.startswith("Downloads/"):
            return downloads / path.replace("Downloads/", "", 1)

        return Path(path)