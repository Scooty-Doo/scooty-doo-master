import os
from .command import Command

class Docker:
    class Compose:
        @staticmethod
        def build(directory, npm=False, reinstall=False):
            if npm and (reinstall or not os.path.exists(os.path.join(directory, 'build'))):
                try:
                    Command.run(["npm", "ci"], directory=directory)
                    print("Running npm install...")
                except Exception as e:
                    print(f"Failed to run NPM install: {e}")
                    print(f"/build exists: {os.path.exists(os.path.join(directory, 'build'))}")
                    return
            if npm:
                try:
                    print("Running npm run build...")
                    Command.run(["npm", "run", "build"], directory=directory)
                except Exception as e:
                    print(f"Failed to run NPM build: {e}")
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
    
    
