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
        with open(file_path, "w") as f:
            f.write("")
        lines = File.Read.lines(file_path)
        assert lines == [], "Should return an empty list for empty file"
