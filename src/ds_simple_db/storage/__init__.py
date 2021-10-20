from ds_simple_db.core.factory import Factory

from .memory_dict_storage import MemoryDictStorage


class StorageFactory(Factory):
    """
    A factory to create storage
    """
    classes = dict(
        memory_dict_storage=MemoryDictStorage
    )
