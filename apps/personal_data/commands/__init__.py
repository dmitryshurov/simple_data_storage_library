from ds_command.command import Command
from ds_simple_db.storage import StorageFactory


class PersonalDataCommand(Command):
    DB_COLUMNS = ['name', 'address', 'phone_number']
    STORAGE_TYPE = 'memory_dict_storage'

    def create_storage(self):
        return StorageFactory.create(self.STORAGE_TYPE, columns=self.DB_COLUMNS)
