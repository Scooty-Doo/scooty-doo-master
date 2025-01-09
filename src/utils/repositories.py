import os
from .directory import Directory
from ..utils.command import Command
from .repository import Repository

LOCAL_REPOSITORIES_DIR = Directory.local_repositories()

class Repositories:
    def __init__(self):
        self.repositories = {
            "backend": "https://github.com/Scooty-Doo/scooty-doo-backend.git",
            "frontend": "https://github.com/Scooty-Doo/scooty-doo-frontend.git",
            "bike": "https://github.com/Scooty-Doo/scooty-doo-bike.git"
        }

        self.local = _Local(repositories=self.repositories)
        self.submodules = _Submodules()

class _Local:
    def __init__(self, repositories):
        self.repositories = dict(repositories)
        os.makedirs(LOCAL_REPOSITORIES_DIR, exist_ok=True)
        self.get = self._Get(repositories=self.repositories)

    class _Get:
        def __init__(self, repositories):
            self.repositories = dict(repositories)

        def _get_repository(self, name, branch=None, force=False):
            repository_url = self.repositories.get(name)
            repository_path = os.path.join(LOCAL_REPOSITORIES_DIR, name)
            if not repository_url:
                raise ValueError(f"Unknown repository: {name}")
            if os.path.isdir(repository_path):
                print(f"Repository {name} already exists locally.")
                if branch:
                    print(f"Switching to branch '{branch}' in {name}...")
                    Repository.fetch(repository_path)
                    Repository.checkout(repository_path, branch)
                    Repository.pull(repository_path, force=force, branch=branch)
                    Repository.Print.commit(repository_path)
                else:
                    print(f"Pulling latest changes in {name} on the current branch...")
                    Repository.pull(repository_path, force=force)
                    Repository.Print.commit(repository_path)
            else:
                print(f"Cloning {name}...")
                Repository.clone(repository_url, repository_path, branch)

        def backend(self, branch=None):
            self._get_repository("backend", branch)

        def frontend(self, branch=None):
            self._get_repository("frontend", branch, force=True)

        def bike(self, branch=None):
            self._get_repository("bike", branch)

        def all(self, branch=None):
            def _print_commits():
                print("Printing commits for all repositories...")
                for name in self.repositories.keys():
                    repository_path = os.path.join(LOCAL_REPOSITORIES_DIR, name)
                    Repository.Print.commit(repository_path)
            self._get_repository("backend", branch)
            self._get_repository("frontend", branch, force=True)
            self._get_repository("bike", branch)
            _print_commits()
            

class _Submodules:
    def __init__(self):
        self.get = self.Get()
        self.deinitialize = self.Deinitialize()

    class Get:
        def all(self):
            """
            Pull all submodules to submodules directory.
            Ensures submodules are initialized and up-to-date.
            """
            def _initialize_submodules():
                """
                Initializes submodules in case they are not initialized.
                Submodules update to their latest commit in the master repository.
                """
                print("Initializing all submodules...")
                Command.run(["git", "submodule", "update", "--init", "--recursive"], raise_exception=True)

            def _update_local_submodules():
                """
                Updates all submodules to the latest commit on the main branch of each submodule.
                """
                print("Updating (pulling) all submodules...")
                Command.run(["git", "submodule", "foreach", "--recursive", "git", "pull", "origin", "main"], raise_exception=True)

            _initialize_submodules()
            _update_local_submodules()

    class Deinitialize:
        def all(self):
            """
            Deinitialize all submodules.
            Submodule references (and folders) are kept but their contents are removed from local repository.
            Remote repositories are not affected.
            """
            print("Deinitializing all submodules...")
            Command.run(["git", "submodule", "deinit", "-f", "--all", ], raise_exception=True)

if __name__ == "__main__":
    repositories = Repositories()
    repositories.local.get.all()
    #repositories.submodules.get.all()
    # repositories.submodules.deinitialize.all()

    # python -m src.utils.repositories
