from ..utils.command import Command

class Repository:
    class Checkout:
        @staticmethod
        def files(repository_path, files: list):
            if not files:
                print("No files to checkout.")
                return
            try:
                Command.run(["git", "-C", repository_path, "checkout", "--", *files], raise_exception=True)
                print(f"Successfully checked out files: {files}")
            except Exception as e:
                print(f"Error checking out files {files}: {e}")
                raise e

    @staticmethod
    def fetch(repository_path):
        Command.run(["git", "-C", repository_path, "fetch"], raise_exception=True)

    @staticmethod
    def checkout(repository_path, branch):
        Command.run(["git", "-C", repository_path, "checkout", branch], raise_exception=True)

    @staticmethod
    def pull(repository_path, force=False, branch=None, commit=None):
        """
        Pull the latest changes from the remote repository.
        
        Args:
            repository_path (str): The path to the local repository.
            force (bool, optional): Whether to force the pull, disregarding any local changes. Defaults to False.
            branch (str, optional): The branch to pull from. Defaults to None, which means "main".
            commit (str, optional): A specific commit hash to pull and reset to. Defaults to None.
        """
        def _pull():
            Command.run(["git", "-C", repository_path, "pull"], raise_exception=True)

        if not force:
            _pull()
            if commit:
                print(f"Resetting repository {repository_path} to commit {commit}...")
                Command.run(["git", "-C", repository_path, "reset", "--hard", commit], raise_exception=True)
        else:
            # METHOD 1 (HEAVY)
            #Repository.fetch(repository_path)
            #branch = "main" if not branch else branch
            #remote_branch = f"origin/{branch}"
            #reset_command = ["git", "-C", repository_path, "reset", "--hard", remote_branch]
            #Command.run(reset_command, raise_exception=True)

            # METHOD 2 (LIGHT)
            files_to_checkout = ["package.json", "package-lock.json"]
            Repository.Checkout.files(repository_path, files_to_checkout)
            _pull()
            if commit:
                print(f"Resetting repository {repository_path} to commit {commit}...")
                Command.run(["git", "-C", repository_path, "reset", "--hard", commit], raise_exception=True)

    @staticmethod
    def clone(repository_url, repository_path, branch=None):
        clone_command = ["git", "clone", repository_url, repository_path]
        if branch:
            clone_command.extend(["-b", branch])
        Command.run(clone_command, raise_exception=True)
    
    class Print:
        @staticmethod
        def commit(repository_path):
            try:
                commit_info = Command.run(
                    ["git", "-C", repository_path, "log", "-1", "--pretty=format:%h - %s"],
                    raise_exception=True
                )
                print(f"Commit after pull in {repository_path}: {commit_info}")
            except Exception as e:
                print(f"Error retrieving commit info after pull: {e}")
