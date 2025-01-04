import os
from .command import Command

class Docker:
    class Compose:
        @staticmethod
        def build(directory, npm=False, reinstall=False):
            if npm:
                print("Running npm install and npm run build...")
                try:
                    if reinstall or not os.path.join(directory, 'build'):
                        Command.run(["npm", "ci"], directory=directory)
                    Command.run(["npm", "ci"], directory=directory)
                    Command.run(["npm", "run", "build"], directory=directory)
                    print("NPM build completed successfully.")
                except Exception as e:
                    print(f"Failed to run NPM commands: {e}")
                    return
            try:
                print("Building the Docker image...")
                Command.run(["docker-compose", "build"], directory=directory)
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
    
    
