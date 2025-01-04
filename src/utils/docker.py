from .command import Command

class Docker:
    class Compose:
        @staticmethod
        def build(directory):
            Command.run(["docker-compose", "build"], directory=directory)

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
    
    
