import os
import json
from tempfile import TemporaryDirectory
from src.utils.file import File

def test_csv_to_json():
    csv_data = "id,name\n1,The Lord\n2,Aragorn"
    result = File.Convert.csv_to_json(csv_data)
    expected = [
        {"id": "1", "name": "The Lord"},
        {"id": "2", "name": "Aragorn"}
    ]
    assert result == expected, "Should correctly parse CSV data into a list of dicts"

def test_file_change_extension():
    new_filename = File.Change.extension("data.txt", ".json")
    assert new_filename == "data.json", "Should replace .txt with .json"

def test_file_change_name():
    new_filename = File.Change.name("data.csv", "new_data")
    assert new_filename == "new_data.csv", "Should rename file while preserving extension"

def test_save_to_json():
    with TemporaryDirectory() as tmpdir:
        data = {"key": "value"}
        filename = "test_output.json"
        File.Save.to_json(data, tmpdir, filename)
        file_path = os.path.join(tmpdir, filename)
        assert os.path.exists(file_path), "JSON file should be created"
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        assert loaded_data == data, "JSON file contents should match data"

def test_read_lines_empty_file():
    with TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "empty_file.txt")
        with open(file=file_path, mode="w", encoding='utf-8') as f:
            f.write("")
        lines = File.Read.lines(file_path)
        assert lines == [], "Should return an empty list for empty file"

def test_load_from_csv():
    with TemporaryDirectory() as tmpdir:
        filename = "test_data.csv"
        file_path = os.path.join(tmpdir, filename)
        csv_content = "id,name\n1,Frodo\n2,Sam"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(csv_content)
        loaded_data = File.Load.from_csv(tmpdir, filename)
        assert loaded_data == csv_content, "Should correctly load CSV content as a string"

def test_read_lines_non_existent_file():
    with TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "non_existent_file.txt")
        lines = File.Read.lines(file_path)
        assert lines == [], "Should return an empty list when file does not exist"

def test_write_lines():
    with TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "output.txt")
        lines_to_write = ["first line", "second line", "third line"]
        File.Write.lines(file_path, lines_to_write)
        with open(file_path, "r", encoding="utf-8") as f:
            written_content = f.read().splitlines()
        assert written_content == lines_to_write, "Should write all lines correctly to the file"
