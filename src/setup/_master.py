from ..utils.docker import Docker
from ..utils.directory import Directory

DATABASE_ADMIN_CONTAINER = "database-adminer-1"
DATABASE_CONTAINER = "database-db-1"
BACKEND_CONTAINER = "api"

class Master:
    @staticmethod
    def _delete_containers():
        Docker.Container.stop(DATABASE_ADMIN_CONTAINER)
        Docker.Container.stop(DATABASE_CONTAINER)
        Docker.Container.stop(BACKEND_CONTAINER)
        Docker.Container.delete(DATABASE_ADMIN_CONTAINER)
        Docker.Container.delete(DATABASE_CONTAINER)
        Docker.Container.delete(BACKEND_CONTAINER)

    @staticmethod
    def setup():
        Master._delete_containers()
        Docker.Compose.up(Directory.root())

if __name__ == "__main__":
    Master.setup()

    # python -m src.setup._master