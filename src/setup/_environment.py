import os
import shutil
from ..utils.extract import Extract
from ..utils.directory import Directory
from ..utils.file import File

ENV_DIR = Directory.env()
REPO_DIR = Directory.repos()

class Environment:
    class Files:
        @staticmethod
        def generate(
            backend: bool = False,
            frontend: bool = False,
            bikes: list[dict] = None
            ):
            """Generate .env files for the backend, frontend, and/or bikes."""

            def _backend():
                Environment._copy_env_file(
                    source_env_filename='.env.backend',
                    target_repo=Directory.Repo.backend())
            def _frontend():
                Environment._copy_env_file(
                    source_env_filename='.env.frontend',
                    target_repo=Directory.Repo.frontend())
            def _bikes(bikes):
                target_repo = Directory.Repo.bike()
                Environment._copy_env_file(
                    source_env_filename='.env.bike',
                    target_repo=target_repo
                )
                bike_ids = Extract.Bike.ids(bikes)
                positions = Extract.Bike.positions(bikes)
                output_env_file = os.path.join(target_repo, '.env')
                lines = File.Read.lines(output_env_file)
                existing_lines = Extract.Lines.not_startswith(lines, ('BIKE_IDS=', 'POSITIONS='))
                new_lines = [
                    f"BIKE_IDS={','.join(map(str, bike_ids))}",
                    f"POSITIONS={','.join(map(str, positions))}"]
                output_env_content = existing_lines + new_lines
                File.Write.lines(output_env_file, output_env_content)
                print(f"Generated .env file for the bikes at '{output_env_file}'.")

            if backend:
                _backend()
            if frontend:
                _frontend()
            if bikes:
                _bikes(bikes)
            if not (backend or frontend or bikes):
                print("At least one of 'backend', 'frontend', or 'bikes' must be True.")

    @staticmethod
    def _copy_env_file(source_env_filename, target_repo):
        env_source_path = os.path.join(ENV_DIR, source_env_filename)
        env_target_path = os.path.join(Directory.Repo.get(target_repo), ".env")
        if not os.path.exists(env_source_path):
            raise FileNotFoundError(f"Source .env file '{env_source_path}' does not exist.")
        target_dir = os.path.dirname(env_target_path)
        if not os.path.exists(target_dir):
            raise FileNotFoundError(f"Target directory '{target_dir}' does not exist.")
        shutil.copyfile(env_source_path, env_target_path)
        print(f"Copied '{env_source_path}' to '{env_target_path}' (replaced if existed).")
