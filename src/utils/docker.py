import os
import platform
from .command import Command

class Docker:
    class Compose:
        @staticmethod
        def build(directory, npm=False, reinstall=False):
            is_windows = platform.system() == "Windows"
            npm_filename = "npm.cmd" if is_windows else "npm"
            def _npm_exists():
                try:
                    Command.run([npm_filename, "--version"], inherit_environment=True)
                    return True
                except Exception as e:
                    return False
            if npm:
                if not _npm_exists():
                    raise Exception("NPM is not installed.")
                if (reinstall or not os.path.exists(os.path.join(directory, 'build'))):
                    try:
                        Command.run([npm_filename, "install"], directory=directory, inherit_environment=True)
                        print("Running npm install...")
                    except Exception as e:
                        print(f"Failed to run NPM install: {e}")
                        print(f"/build exists: {os.path.exists(os.path.join(directory, 'build'))}")
                        return
                try:
                    print("Running npm run build...")
                    Command.run([npm_filename, "run", "build"], directory=directory, inherit_environment=True)
                    Command.run(["docker-compose", "up", "webclient-prod", "-d"], directory=directory)
                except Exception as e:
                    print(f"Failed to run NPM build: {e}")
                    return
            if not npm:
                try:
                    print("Building the Docker image...")
                    Command.run(["docker-compose", "up", "-d"], directory=directory)
                    print("Docker image built successfully.")    
                except Exception as e:
                    print(f"Failed to build the Docker image: {e}")

        @staticmethod
        def up(directory):
            Command.run(["docker-compose", "up", "-d"], directory=directory)

        @staticmethod
        def down(directory):
            Command.run(["docker-compose", "down"], directory=directory)
        
        @staticmethod
        def restart(directory):
            Docker.Compose.down(directory)
            Docker.Compose.up(directory)
        
        @staticmethod
        def status(directory):
            Command.run(["docker-compose", "ps"], directory=directory)
    
    
