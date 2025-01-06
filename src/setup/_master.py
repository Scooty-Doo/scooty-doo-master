import os
from ..utils.docker import Docker
from ..utils.directory import Directory

REPO_DIR = Directory.root()
DATABASE_CONTAINER = os.getenv("DATABASE_CONTAINER", 'database-db-1')
DATABASE_ADMINER_CONTAINER = os.getenv("DATABASE_ADMINER_CONTAINER", 'database-adminer-1')
BACKEND_CONTAINER = os.getenv("BACKEND_CONTAINER", 'api')
BIKE_CONTAINER = os.getenv("BIKE_CONTAINER", 'bike_hivemind_app')

class Master:
    class Docker:
        @staticmethod
        def clear():
            Docker.Container.delete(DATABASE_CONTAINER)
            Docker.Container.delete(DATABASE_ADMINER_CONTAINER)
            Docker.Container.delete(BACKEND_CONTAINER)
            Docker.Container.delete(BIKE_CONTAINER)

        @staticmethod
        def build():
            Docker.Compose.build(REPO_DIR)

        @staticmethod
        def up():
            Docker.Compose.up(REPO_DIR)
        
        @staticmethod
        def down():
            Docker.Compose.down(REPO_DIR)
        
        @staticmethod
        def status():
            Docker.Compose.status(REPO_DIR)
        
        @staticmethod
        def logs():
            Docker.Compose.logs(REPO_DIR)
        
        @staticmethod
        def restart():
            Master.Docker.down()
            Master.Docker.clear()
            Master.Docker.build()
            Master.Docker.up()
            Master.Docker.status()
            Master.Docker.logs()
        
    @staticmethod
    def setup():
        Master.Docker.restart()


if __name__ == "__main__":
    Master.setup()

    # python -m src.setup._master