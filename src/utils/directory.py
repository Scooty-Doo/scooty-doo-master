import os
from .settings import Settings

class Directory:
    @staticmethod
    def root():
        return os.getcwd()
    
    @staticmethod
    def database():
        return os.path.join(Directory.Repo.backend(), Settings.Directory.Name.database)
    
    @staticmethod
    def mocked_data():
        return os.path.join(Directory.root(), Settings.Directory.mocked_data)

    @staticmethod
    def env():
        return os.path.join(Settings.Directory.env)
    
    @staticmethod
    def env_example():
        return os.path.join(Directory.env(), 'example')
    
    @staticmethod
    def venv(repo_dir):
        return os.path.join(repo_dir, Settings.Directory.Name.venv)
    
    @staticmethod
    def repos():
        return os.path.join(Directory.root(), Settings.Directory.repos)

    class Repo:
        @staticmethod
        def backend():
            return Directory.Repo.get(Settings.Directory.Name.backend)
        
        @staticmethod
        def frontend():
            return Directory.Repo.get(Settings.Directory.Name.frontend)
        
        @staticmethod
        def bike():
            return Directory.Repo.get(Settings.Directory.Name.bike)

        @staticmethod
        def get(name):
            return os.path.join(Directory.root(), Settings.Directory.repos, name)