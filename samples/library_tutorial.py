import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')

print()
print('===========================================')
print('Creating a new storage and adding some data')
print('===========================================')

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


print()
print('==================')
print('Retrieving entries')
print('==================')

# Retrieve all entries from the storage
all_entries = storage.all_entries()
print('All entries:', all_entries)


print()
print('=================')
print('Filtering entries')
print('=================')

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


print()
print('===================')
print('Serializing entries')
print('===================')

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


print()
print('====================================')
print('Deserializing strings to entry lists')
print('====================================')

# Deserializing JSON
json_str = '{"entries": [{"name": "Sergey", "address": "St. Petersburg"}, {"name": "Alex", "address": null}]}'
print('JSON string to deserialize: ', json_str)
print('Deserialized JSON entries: ', json_serializer.entries_from_string(json_str), '\n')

# Deserializing CSV
csv_str = '#name,address\nSergey,St. Petersburg\nAlex,'
print('CSV string to deserialize:\n', csv_str, '\n', sep='')
print('Deserialized CSV entries: ', csv_serializer.entries_from_string(csv_str))


print()
print('===========================')
print('Loading and saving database')
print('===========================')

# Load the data from `example.csv` and append it to the currently existing data in the storage
storage.load_from_file("db/example.csv")

# Save the data to `example.json`
storage.save_to_file("db/example.json")

print("See db/example.json to view the result\n")
