# pylint: disable=protected-access, too-few-public-methods
"""Module to manage the setup of the environment."""

import os
import shutil
from ..utils.directory import Directory

ROOT_DIR = Directory.root()
ENV_EXAMPLE_DIR = Directory.env_example()
ENV_DIR = Directory.env()
REPO_DIR = Directory.repositories()

class Environment:
    """Environment class to manage the setup of the environment."""
    class Files:
        """Class to manage the setup of the environment files."""
        @staticmethod
        def _setup():
            """
            Copies '/env/example/' .env files ('.env.backend.example' etc.) to '/env/' 
            and removes '*.example' from the filenames.
            Does not overwrite existing files.
            """
            def _root_env():
                """Copies the root .env file."""
                if not os.path.exists(os.path.join(ROOT_DIR, '.env')):
                    example_env_path = os.path.join(ROOT_DIR, '.env.example')
                    env_path = os.path.join(ROOT_DIR, '.env')
                    if not os.path.exists(example_env_path):
                        raise FileNotFoundError(
                            f"Example .env file '{example_env_path}' does not exist.")
                    if not os.path.exists(env_path):
                        shutil.copyfile(example_env_path, env_path)

            def _repositories_env():
                """Copies the repository .env files."""
                for env_example_file in os.listdir(ENV_EXAMPLE_DIR):
                    if env_example_file.endswith('.example'):
                        env_example_path = os.path.join(ENV_EXAMPLE_DIR, env_example_file)
                        env_path = os.path.join(ENV_DIR, env_example_file.replace('.example', ''))
                        if not os.path.exists(env_path):
                            shutil.copyfile(env_example_path, env_path)
                            print(
                                f"Copied '{env_example_path}' \
                                    to '{env_path}' (replaced if existed).")
                        else:
                            print(f"File '{env_path}' already exists. Skipping.")
            _root_env()
            _repositories_env()

        @staticmethod
        def generate(
            master: bool = True,
            backend: bool = True,
            frontend: bool = True,
            bikes: bool = True
            ):
            """Generate .env files for the backend, frontend, and/or bikes."""

            if master:
                Environment.Files._setup()

            def _backend():
                """Copies the backend .env file."""
                Environment._copy_env_file(
                    source_env_filename='.env.backend',
                    target_repo=Directory.Repo.backend())
            def _frontend():
                """Copies the frontend .env file."""
                Environment._copy_env_file(
                    source_env_filename='.env.frontend',
                    target_repo=Directory.Repo.frontend())
            def _bikes():
                """Copies the bikes .env file."""
                Environment._copy_env_file(
                    source_env_filename='.env.bike',
                    target_repo=Directory.Repo.bike()
                )

            if backend:
                _backend()
            if frontend:
                _frontend()
            if bikes:
                _bikes()
            if not (backend or frontend or bikes):
                print("At least one of 'backend', 'frontend', or 'bikes' must be True.")

    @staticmethod
    def _copy_env_file(source_env_filename, target_repo):
        """Copy the source .env file to the target repository."""
        env_source_path = os.path.join(ENV_DIR, source_env_filename)
        env_target_path = os.path.join(Directory.Repo.get(target_repo), ".env")
        if not os.path.exists(env_source_path):
            raise FileNotFoundError(f"Source .env file '{env_source_path}' does not exist.")
        target_dir = os.path.dirname(env_target_path)
        if not os.path.exists(target_dir):
            raise FileNotFoundError(f"Target directory '{target_dir}' does not exist.")
        shutil.copyfile(env_source_path, env_target_path)
        print(f"Copied '{env_source_path}' to '{env_target_path}' (replaced if existed).")
