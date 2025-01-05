import json
import os

class File:
    class Save:
        @staticmethod
        def to_json(data, folder, filename):
            filename = File.Change.extension(filename, '.json')
            path = os.path.join(folder, filename)
            with open(file=path, mode='w', encoding='utf-8') as file:
                json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)

    class Load:
        @staticmethod
        def from_csv(folder, filename):
            path = os.path.join(folder, filename)
            with open(file=path, mode='r', encoding='utf-8') as file:
                return file.read()

    class Convert:
        @staticmethod
        def csv_to_json(csv_data):
            lines = csv_data.splitlines()
            headers = lines[0].split(',')
            data = []
            for line in lines[1:]:
                values = line.split(',')
                data.append(dict(zip(headers, values)))
            return data

    class Change:
        @staticmethod
        def extension(filename, new_extension):
            return os.path.splitext(filename)[0] + new_extension

        @staticmethod
        def name(filename, new_name):
            extension = os.path.splitext(filename)[1]
            new_name = new_name + extension
            return new_name

    class Read:
        @staticmethod
        def lines(file):
            if os.path.exists(file):
                with open(file=file, mode='r', encoding='utf-8') as file:
                    return file.readlines()
            else:
                print("File does not exist.")
                return []

    class Write:
        @staticmethod
        def lines(file, lines):
            with open(file=file, mode='w', encoding='utf-8') as file:
                file.writelines('\n'.join(lines) + '\n')
