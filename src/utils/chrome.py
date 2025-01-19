import platform
from ..utils.command import Command

CHROME_EXECUTABLE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
IS_WINDOWS = platform.system() == "Windows"

class Chrome:
    class Open:
        @staticmethod
        def window(*ports):
            if IS_WINDOWS:
                if ports:
                    urls = [f"http://localhost:{port}" for port in ports if port]
                    Command.run([CHROME_EXECUTABLE] + ["--new-tab"] + urls)
                    print("Please manually refresh the tabs if they do not load.")
                else:
                    Command.run([CHROME_EXECUTABLE])
            else:
                print("If not on Windows, please open Chrome window manually.")
