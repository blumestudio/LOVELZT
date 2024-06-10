import os
import threading
from collections import defaultdict


class FileManager:
    def __init__(self, base_path="files"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        self.locks = {}
        self.versions = {}
        self.global_lock = threading.Lock()
        self.file_watchers = defaultdict(list)

    def _get_lock(self, filename):
        with self.global_lock:
            if filename not in self.locks:
                self.locks[filename] = threading.Lock()
            return self.locks[filename]

    def read_file(self, filename):
        lock = self._get_lock(filename)
        with lock:
            try:
                with open(os.path.join(self.base_path, filename), "r") as file:
                    return file.read()
            except FileNotFoundError:
                return "File not found"

    def write_file(self, filename, content):
        lock = self._get_lock(filename)
        with lock:
            if filename in self.versions:
                version = self.versions[filename] + 1
            else:
                version = 1
            self.versions[filename] = version
            versioned_filename = f"{filename}.v{version}"
            with open(os.path.join(self.base_path, filename), "w") as file:
                file.write(content)
            with open(os.path.join(self.base_path, versioned_filename), "w") as versioned_file:
                versioned_file.write(content)

            # Оповещаем всех подписчиков об изменении файла
            for watcher in self.file_watchers[filename]:
                watcher.send(content)

    def get_versions(self, filename):
        return [f for f in os.listdir(self.base_path) if f.startswith(filename)]

    def watch_file(self, filename, watcher):
        self.file_watchers[filename].append(watcher)
