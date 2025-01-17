# pylint: disable=too-few-public-methods
"""Module to manage the repositories of the project."""

import os
from .directory import Directory
from ..utils.command import Command
from .repository import Repository

LOCAL_REPOSITORIES_DIR = Directory.local_repositories()

class Repositories:
    """Class to manage the repositories of the project."""
    def __init__(self):
        self.repositories = {
            "backend": "https://github.com/Scooty-Doo/scooty-doo-backend.git",
            "frontend": "https://github.com/Scooty-Doo/scooty-doo-frontend.git",
            "bike": "https://github.com/Scooty-Doo/scooty-doo-bike.git"
        }

        self.local = _Local(repositories=self.repositories)
        self.submodules = _Submodules()

class _Local:
    """Class to manage the local repositories of the project."""
    def __init__(self, repositories): # pylint: disable=redefined-outer-name
        self.repositories = dict(repositories)
        os.makedirs(LOCAL_REPOSITORIES_DIR, exist_ok=True)
        self.get = self._Get(repositories=self.repositories)

    class _Get:
        """Class to get the local repositories."""
        def __init__(self, repositories): # pylint: disable=redefined-outer-name
            self.repositories = dict(repositories)

        def _get_repository(self, name, branch=None, force=False, commit=None):
            """Get a specific repository."""
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
                    if commit:
                        print(f"Resetting to commit {commit} in {name} on branch '{branch}'...")
                        Repository.pull(repository_path, force=force, branch=branch, commit=commit)
                    else:
                        Repository.pull(repository_path, force=force, branch=branch)
                    Repository.Print.commit(repository_path)
                else:
                    if commit:
                        print(f"Resetting to commit {commit} in {name} on the current branch...")
                        Repository.pull(repository_path, force=force, commit=commit)
                    else:
                        print(f"Pulling latest changes in {name} on the current branch...")
                        Repository.pull(repository_path, force=force)
                    Repository.Print.commit(repository_path)
            else:
                print(f"Cloning {name}...")
                Repository.clone(repository_url, repository_path, branch)
                if branch:
                    print(f"Switching to branch '{branch}' in {name}...")
                    Repository.checkout(repository_path, branch)
                if commit:
                    print(f"Resetting to commit {commit} in {name}...")
                    Repository.pull(repository_path, commit=commit)
                Repository.Print.commit(repository_path)

        def backend(self, branch=None, commit=None):
            """Get the backend repository."""
            self._get_repository("backend", branch=branch, commit=commit)

        def frontend(self, branch=None, commit=None):
            """Get the frontend repository."""
            self._get_repository("frontend", branch=branch, force=True, commit=commit)

        def bike(self, branch=None, commit=None):
            """Get the bike repository."""
            self._get_repository("bike", branch=branch, commit=commit)

        def all(self, branch=None):
            """Get all repositories."""
            def _print_commits():
                """Print the commits for all repositories."""
                print("Printing commits for all repositories...")
                for name in self.repositories.keys():
                    repository_path = os.path.join(LOCAL_REPOSITORIES_DIR, name)
                    Repository.Print.commit(repository_path)
            self._get_repository("backend", branch)
            self._get_repository("frontend", branch, force=True)
            self._get_repository("bike", branch)
            _print_commits()


class _Submodules:
    """Class to manage the submodules of the project."""
    def __init__(self):
        self.get = self.Get()
        self.deinitialize = self.Deinitialize()

    class Get:
        """Class to get the submodules of the project."""
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
                Command.run(
                    ["git", "submodule", "update", "--init", "--recursive"],
                    raise_exception=True)

            def _update_local_submodules():
                """
                Updates all submodules to the latest commit on the main branch of each submodule.
                """
                print("Updating (pulling) all submodules...")
                Command.run(
                    ["git", "submodule", "foreach", "--recursive", "git",
                     "pull", "origin", "main"], raise_exception=True)

            _initialize_submodules()
            _update_local_submodules()

    class Deinitialize:
        """Class to deinitialize the submodules of the project."""
        def all(self):
            """
            Deinitialize all submodules.
            Submodule references (and folders) are kept but their contents
            are removed from local repository.
            Remote repositories are not affected.
            """
            print("Deinitializing all submodules...")
            Command.run(["git", "submodule", "deinit", "-f", "--all", ], raise_exception=True)

if __name__ == "__main__": # pragma: no cover
    repositories = Repositories()
    repositories.local.get.all()
    #repositories.submodules.get.all()
    # repositories.submodules.deinitialize.all()

    # python -m src.utils.repositories
