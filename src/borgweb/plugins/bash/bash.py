from borgweb.plugins import Plugin
import subprocess

class Bash(Plugin):
    backend_only = True
    plugin_name = "bash"

    def setup_routes(self):
        pass


    def __init__(self, capture_output=True, text_mode=True):
        """
        Initializes the BashRunner.

        :param capture_output: Boolean to determine if stdout and stderr should be captured.
        :param text_mode: Boolean to determine if output should be treated as text.
        """
        self.capture_output = capture_output
        self.text_mode = text_mode

    def run(self, command):
        """
        Executes a Bash command.

        :param command: The command string to execute.
        :return: A dictionary with keys 'stdout', 'stderr', and 'returncode'.
        """
        try:
            result = subprocess.run(
                command,
                capture_output=self.capture_output,
                text=self.text_mode,
                check=True
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.CalledProcessError as e:
            # If the command fails (non-zero exit), return the error details.
            return {
                'stdout': e.stdout,
                'stderr': e.stderr,
                'returncode': e.returncode
            }