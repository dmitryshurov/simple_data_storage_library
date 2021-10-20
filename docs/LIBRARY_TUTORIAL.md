# How to use and extend the library

## Adding the library to your project

To add the library to your project just add the [src](../src) folder to your `PYTHONPATH`.

## Library structure

The library package [ds_simple_db](../src/ds_simple_db) consists of the following sub-packages:
* `core` - core classes and interfaces
* `filters` - implementations of filters
* `serializers` - implementations of serializers
* `storage` - implementations of storage types

Read below to learn how to implement your own filters/serializer/storage.

There is also a small [ds_command](../src/ds_command) library that simplifies creation of command-line apps, but it is straightforward and won't be discussed here. Please see the 

## Library core
The [core](../src/ds_simple_db/core) package contains the following classes. Please read docstrings to each class to learn the details about their implementation and structure.

* `Storage` - The base class for all storage types that provide underlying structures to store data. Storage can be persistent (e.g., databases) or non-persistent (in-memory). Currently only an in-memory `MemoryDictStorage` is implemented. Note that storage is different from a serializer since it provides an interface to the core database while serializers just serialize/deserialize data to/from strings. 
* `Entry` - Represents data that is retrieved from the storage. Each entry contains a set of fields and their corresponding values.
* `Serializer` - The base class for all serializers that serialize/deserialize data to/from strings. Currently serializers for `JSON` and `CSV` format are implemented.
* `Filter` - The base class for all filters applied to the entries of a storage. Currently only `GlobFilter` is implemented.

There is also a helper `Factory` class that helps to create new factories for other entities.

## Using the library: step-by-step

The complete runnable sample code for this section can be found in [library_tutorial.py](../samples/library_tutorial.py).

You can run it by running the following command from the repository root (no need to set PYTHONPATH manually):

```shell script
python3 samples/library_tutorial.py
```

### Creating a new storage and adding some data

```python
from ds_simple_db.storage import StorageFactory

# List available storage types
print('Available storage types:', StorageFactory.list())

# Create a built-in storage type `memory_dict_storage`
# Define a list of columns to keep in the storage
storage = StorageFactory.create(
    'memory_dict_storage',
    columns=['name', 'address', 'phone_number']
)

# Insert 2 entries. Unspecified fields are filled with `None`
storage.insert(name='Dmitry', address='Moscow')
storage.insert(name='Andrew')
```

### Retrieving entries

```python
# Retrieve all entries from the storage
all_entries = storage.all_entries()
print('All entries:', all_entries)
```

### Filtering entries

```python
# Import a built-in GlobFilter class
from ds_simple_db.filters.glob_filter import GlobFilter

# Filter using exact field value
filter_exact = GlobFilter('address=Moscow')
filtered_entries_exact = storage.filter(filter_exact)
print(f'Filtered entries `{filter_exact}`:', filtered_entries_exact)

# Filter using a glob syntax
filter_glob = GlobFilter('name=*r*')
filtered_entries_glob = storage.filter(filter_glob)
print(f'Filtered entries `{filter_glob}`:', filtered_entries_glob)
```

### Serializing entries

```python
from ds_simple_db.serializers import SerializerFactory

# List available serializer types
print('Available serializer types:', SerializerFactory.list(), '\n')

# Serializing to JSON
json_serializer = SerializerFactory.create('json')
print('All entries serialized to JSON:', json_serializer.entries_to_string(all_entries), '\n')
print('Filtered entries serialized to JSON:', json_serializer.entries_to_string(filtered_entries_exact), '\n')

# Serializing to CSV
csv_serializer = SerializerFactory.create('csv')
print('All entries serialized to CSV:\n', csv_serializer.entries_to_string(all_entries), sep='')
print('Filtered entries serialized to CSV:\n', csv_serializer.entries_to_string(filtered_entries_exact), sep='')
```

### Deserializing strings to entry lists

```python
# Deserializing JSON
json_str = '{"entries": [{"name": "Sergey", "address": "St. Petersburg"}, {"name": "Alex", "address": null}]}'
print('JSON string to deserialize: ', json_str)
print('Deserialized JSON entries: ', json_serializer.entries_from_string(json_str), '\n')

# Deserializing CSV
csv_str = '#name,address\nSergey,St. Petersburg\nAlex,'
print('CSV string to deserialize:\n', csv_str, '\n', sep='')
print('Deserialized CSV entries: ', csv_serializer.entries_from_string(csv_str))
```

### Loading and saving database

The following functions are used to save and load the data from files in supported serialization/deserialization formats.

Note that currently the name of the serializer in a `SerializerFactory` must be equal to the file extension.

```python
# Load the data from `example.csv` and append it to the currently existing data in the storage
storage.load_from_file("db/example.csv")

# Save the data to `example.json`
storage.save_to_file("db/example.json")
```

## Running tests

All tests in a project are written using a standard Python unittest library.

To run the tests from the command line type the following:
```shell script
cd src    # This is not required if `src` in in your PYTHONPATH
python3 -m unittest discover -s ../tests
```

## Extending the library

The library is designed to be extensible with custom types of serializers, filters, and storage types.

### Creating your own serializers

To create your own serializer:
1. Chose a name for your serializer, say `MySerializer`
2. Add a file `my_serializer.py` to [serializers](../src/ds_simple_db/serializers) package
3. In `my_serializer.py` create a class that inherits from the `Serializer` class: 
    ```python
    from typing import List
    
    from ds_simple_db.core.entry import Entry
    from ds_simple_db.core.serializer import Serializer
    
    
    class MySerializer(Serializer):
        def entries_to_string(self, entries: List[Entry]) -> str:
            pass
    
        def entries_from_string(self, input_str: str) -> List[Entry]:
            pass
    ```
4. Implement `entries_to_string()` and `entries_from_string()` methods. You can refer to one of the existing [serializers](../src/ds_simple_db/serializers) and to the [Serializer](../src/ds_simple_db/core/serializer.py) documentation for details.

5. Don't forget to write tests for the new serializer (or even before implementing one). You can refer to existing [serializer tests](../tests/test_ds_simple_db/test_serializers) for details.

6. Add the serializer to the [SerializerFactory](../src/ds_simple_db/serializers/__init__.py) by adding additional key-value pair to the `classes` field. In our example it could be:
```python
    classes = dict(
        csv=CSVSerializer,
        json=JSONSerializer,
        my=MySerializer  # Our new serializer
    )
```

### Creating your own filters
To create your own filter:
1. Chose a name for your serializer, say `MyFilter`
2. Add a file `my_filter.py` to [filters](../src/ds_simple_db/filters) package
3. In `my_filter.py` create a class that inherits from the `Filter` class: 
    ```python
    from ds_simple_db.core.entry import Entry
    from ds_simple_db.core.filter import Filter
    
    
    class MyFilter(Filter):
    
        def __init__(self, filter_str: str):
            # Initialize filter here
            pass
    
        def satisfies(self, entry: Entry) -> bool:
            # Do the actual test here
            pass
    ```
4. Implement `__init__()` and `satisfies()` methods. You can refer to one of the existing [filters](../src/ds_simple_db/filters) for details.

5. Don't forget to write tests for the new filter (or even before implementing one). You can refer to existing [filter tests](../tests/test_ds_simple_db/test_filters) for details.

6. There is no `FilterFactory` yet, but you might consider creating one as in [SerializerFactory](../src/ds_simple_db/serializers/__init__.py).

### Creating your own storage types

To create your own storage type:
1. Chose a name for your serializer, say `MyStorage`
2. Add a file `my_storage.py` to [storage](../src/ds_simple_db/storage) package
3. In `my_storage.py` create a class that inherits from the `Storage` class: 
    ```python
    from typing import List
    
    from ds_simple_db.core.entry import Entry
    from ds_simple_db.core.filter import Filter
    from ds_simple_db.core.storage import Storage
    
    
    class MyStorage(Storage):
        def __init__(self, initial_data: dict = None, columns: list = None):
            pass
    
        def columns(self) -> list:
            pass
    
        def insert(self, **kwargs) -> Entry:
            pass
    
        def all_entries(self) -> List[Entry]:
            pass
    
        def filter(self, filter_obj: Filter = None) -> List[Entry]:
            pass
    ```
4. Implement `__init__()`, `columns()`, `insert()`, `all_entries()`, `filter()` methods. You can refer to one of the existing [storage types](../src/ds_simple_db/storage) and to the [Storage](../src/ds_simple_db/core/storage.py) documentation for details.

5. Don't forget to write tests for the new storage (or even before implementing one). You can refer to existing [storage tests](../tests/test_ds_simple_db/test_storage) for details.

6. Add the storage to the [StorageFactory](../src/ds_simple_db/stotage/__init__.py) by adding additional key-value pair to the `classes` field. In our example it could be:
```python
    classes = dict(
        memory_dict_storage=MemoryDictStorage,
        my_storage=MyStorage  # Our new storage
    )
```