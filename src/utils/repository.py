from ..utils.command import Command

class Repository:
    @staticmethod
    def fetch(repository_path):
        Command.run(["git", "-C", repository_path, "fetch"], raise_exception=True)
    
    @staticmethod
    def checkout(repository_path, branch):
        Command.run(["git", "-C", repository_path, "checkout", branch], raise_exception=True)
    
    @staticmethod
    def pull(repository_path):
        Command.run(["git", "-C", repository_path, "pull"], raise_exception=True)
    
    @staticmethod
    def clone(repository_url, repository_path, branch=None):
        clone_command = ["git", "clone", repository_url, repository_path]
        if branch:
            clone_command.extend(["-b", branch])
        Command.run(clone_command, raise_exception=True)
