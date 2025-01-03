import os
import subprocess

class Repos:
    def __init__(self, base_dir="repos"):
        self.repos = {
            "backend": "https://github.com/Scooty-Doo/scooty-doo-backend.git",
            "frontend": "https://github.com/Scooty-Doo/scooty-doo-frontend.git",
            "bike": "https://github.com/Scooty-Doo/scooty-doo-bike.git"
        }
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        self.get = self.Get(base_dir=self.base_dir, repos=self.repos)

    class Get:
        def __init__(self, base_dir, repos):
            self.base_dir = base_dir
            self.repos = dict(repos)

        def _get_repo(self, name, branch=None):
            repo_url = self.repos.get(name)
            if not repo_url:
                raise ValueError(f"Unknown repository: {name}")

            repo_path = os.path.join(self.base_dir, name)

            if os.path.isdir(repo_path):
                print(f"Repository {name} already exists locally.")
                if branch:
                    print(f"Switching to branch '{branch}' in {name}...")
                    subprocess.run(["git", "-C", repo_path, "fetch"], check=True)
                    subprocess.run(["git", "-C", repo_path, "checkout", branch], check=True)
                    subprocess.run(["git", "-C", repo_path, "pull"], check=True)
                else:
                    print(f"Pulling latest changes in {name} on the current branch...")
                    subprocess.run(["git", "-C", repo_path, "pull"], check=True)
            else:
                print(f"Cloning {name}...")
                clone_cmd = ["git", "clone", repo_url, repo_path]
                if branch:
                    clone_cmd.extend(["-b", branch])
                subprocess.run(clone_cmd, check=True)

        def backend(self, branch=None):
            self._get_repo("backend", branch)

        def frontend(self, branch=None):
            self._get_repo("frontend", branch)

        def bike(self, branch=None):
            self._get_repo("bike", branch)

        def all(self, branch=None):
            for name in self.repos.keys():
                self._get_repo(name, branch)

# Example usage:
if __name__ == "__main__":
    repos = Repos()

    # Fetch all repos
    #repos.get.all()

    repos.get.backend(branch="main")

    repos.get.frontend(branch="main")
    repos.get.bike(branch="main")

    # python -m get_repos