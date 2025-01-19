# pylint: disable=too-few-public-methods
"""Module to manage file operations."""

import json
import os

class File:
    """Class to manage file operations."""
    class Save:
        """Class to manage file saving operations."""
        @staticmethod
        def to_json(data, folder, filename):
            """Save data to a JSON file."""
            filename = File.Change.extension(filename, '.json')
            path = os.path.join(folder, filename)
            with open(file=path, mode='w', encoding='utf-8') as file:
                json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)

    class Load:
        """Class to manage file loading operations."""
        @staticmethod
        def from_csv(folder, filename):
            """Load data from a CSV file."""
            path = os.path.join(folder, filename)
            with open(file=path, mode='r', encoding='utf-8') as file:
                return file.read()

    class Convert:
        """Class to manage file conversion operations."""
        @staticmethod
        def csv_to_json(csv_data):
            """Convert CSV data to JSON data."""
            lines = csv_data.splitlines()
            headers = lines[0].split(',')
            data = []
            for line in lines[1:]:
                values = line.split(',')
                data.append(dict(zip(headers, values)))
            return data

    class Change:
        """Class to manage file name changes."""
        @staticmethod
        def extension(filename, new_extension):
            """Change the extension of a file."""
            return os.path.splitext(filename)[0] + new_extension

        @staticmethod
        def name(filename, new_name):
            """Change the name of a file."""
            extension = os.path.splitext(filename)[1]
            new_name = new_name + extension
            return new_name

    class Read:
        """Class to manage file reading operations."""
        @staticmethod
        def lines(filepath):
            """Read lines from a file."""
            if os.path.exists(filepath):
                with open(filepath, mode='r', encoding='utf-8') as file:
                    return file.readlines()
            else:
                print("File does not exist.")
                return []

    class Write:
        """Class to manage file writing operations."""
        @staticmethod
        def lines(filepath, lines):
            """Write lines to a file."""
            with open(filepath, mode='w', encoding='utf-8') as file:
                file.writelines('\n'.join(lines) + '\n')
