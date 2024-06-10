import subprocess

class GitManager:
    def run_command(self, command):
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Git command failed: {result.stderr}")
        return result.stdout

    def commit(self, message):
        try:
            self.run_command(["git", "commit", "-am", message])
        except Exception as e:
            raise Exception(f"Commit failed: {e}")

    def push(self):
        try:
            self.run_command(["git", "push"])
        except Exception as e:
            raise Exception(f"Push failed: {e}")

    def pull(self):
        try:
            self.run_command(["git", "pull"])
        except Exception as e:
            raise Exception(f"Pull failed: {e}")
