from ..utils.settings import Settings
from ..utils.file import File
from ..utils.directory import Directory

MOCKED_DATA_DIR = Directory.mocked_data()

class Fallback:

    @staticmethod
    def bikes(save_to_json=True):
        filename = Settings.Filenames.Mocked.bikes
        data = File.Load.from_csv(MOCKED_DATA_DIR, filename)
        result = File.Convert.csv_to_json(data)
        filename = File.Change.name(Settings.Filenames.Mocked.bikes, 'bikes')
        if save_to_json:
            File.Save.to_json(data=result, folder=Settings.Directory.data, filename=filename)
        return result

    @staticmethod
    def trips(save_to_json=True):
        filename = Settings.Filenames.Mocked.trips
        data = File.Load.from_csv(MOCKED_DATA_DIR, filename)
        result = File.Convert.csv_to_json(data)
        filename = File.Change.name(Settings.Filenames.Mocked.trips, 'trips')
        if save_to_json:
            File.Save.to_json(data=result, folder=Settings.Directory.data, filename=filename)
        return result

    @staticmethod
    def users(save_to_json=True):
        filename = Settings.Filenames.Mocked.users
        data = File.Load.from_csv(MOCKED_DATA_DIR, filename)
        result = File.Convert.csv_to_json(data)
        filename = File.Change.name(Settings.Filenames.Mocked.users, 'users')
        if save_to_json:
            File.Save.to_json(data=result, folder=Settings.Directory.data, filename=filename)
        return result

    @staticmethod
    def zones(save_to_json=True):
        filename = Settings.Filenames.Mocked.zones
        data = File.Load.from_csv(MOCKED_DATA_DIR, filename)
        result = File.Convert.csv_to_json(data)
        filename = File.Change.name(Settings.Filenames.Mocked.zones, 'zones')
        if save_to_json:
            File.Save.to_json(data=result, folder=Settings.Directory.data, filename=filename)
        return result

    @staticmethod
    def zone_types(save_to_json=True):
        filename = Settings.Filenames.Mocked.zone_types
        data = File.Load.from_csv(MOCKED_DATA_DIR, filename)
        result = File.Convert.csv_to_json(data)
        filename = File.Change.name(Settings.Filenames.Mocked.zone_types, 'zone_types')
        if save_to_json:
            File.Save.to_json(data=result, folder=Settings.Directory.data, filename=filename)
        return result
