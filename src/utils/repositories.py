import os
import subprocess
from .directory import Directory

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

        def _get_repository(self, name, branch=None):
            repository_url = self.repositories.get(name)
            if not repository_url:
                raise ValueError(f"Unknown repository: {name}")

            repository_path = os.path.join(LOCAL_REPOSITORIES_DIR, name)

            if os.path.isdir(repository_path):
                print(f"Repository {name} already exists locally.")
                if branch:
                    print(f"Switching to branch '{branch}' in {name}...")
                    subprocess.run(["git", "-C", repository_path, "fetch"], check=True)
                    subprocess.run(["git", "-C", repository_path, "checkout", branch], check=True)
                    subprocess.run(["git", "-C", repository_path, "pull"], check=True)
                else:
                    print(f"Pulling latest changes in {name} on the current branch...")
                    subprocess.run(["git", "-C", repository_path, "pull"], check=True)
            else:
                print(f"Cloning {name}...")
                clone_cmd = ["git", "clone", repository_url, repository_path]
                if branch:
                    clone_cmd.extend(["-b", branch])
                subprocess.run(clone_cmd, check=True)

        def backend(self, branch=None):
            self._get_repository("backend", branch)

        def frontend(self, branch=None):
            self._get_repository("frontend", branch)

        def bike(self, branch=None):
            self._get_repository("bike", branch)

        def all(self, branch=None):
            for name in self.repositories.keys():
                self._get_repository(name, branch)

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
                subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True)

            def _update_submodules():
                """
                Updates all submodules to the latest commit on the main branch of each submodule.
                """
                print("Updating (pulling) all submodules...")
                subprocess.run(["git", "submodule", "foreach", "--recursive", "git", "pull", "origin", "main"], check=True)

            _initialize_submodules()
            _update_submodules()

    class Deinitialize:
        def all(self):
            """
            Deinitialize all submodules.
            Submodule references (and folders) are kept but their contents are removed from local repository.
            Remote repositories are not affected.
            """
            print("Deinitializing all submodules...")
            subprocess.run(["git", "submodule", "deinit", "-f", "--all", ], check=True)
