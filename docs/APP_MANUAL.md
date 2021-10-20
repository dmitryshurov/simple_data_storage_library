# How to use the app

## Introduction

The app to insert/filter/display the data is a python script located at [personal_data.py](../apps/personal_data.py).

You'll need Python 3.7 set up to run the app.

The script supports several [commands](../apps/personal_data/commands):
* `insert` - insert a single entry to a dataset (and create a dataset if it does not exist)
* `display`- display all entries in a dataset
* `filter` - display entries in a dataset matching a given filter
* `convert` - save a dataset to another (or even the same) format

## Running the app

To to run the app one needs to specify a command (one of the above) and its arguments. Each command has its own set of arguments.

All of the examples below imply that the app is being run from the repository root. You are free to run it from any folder, though.

To run the app one should follow the pattern:

```shell script
python3 apps/personal_data.py <command> --path <path_to_db> <command_args>
```
where `path_to_db` is a path to the database file in one of the supported serialization formats.

## Running the commands

To get started with the app just run the commands below sequentially.

### Insert

To create a `db/demo.csv` file and insert the first entry:

```shell script
python3 apps/personal_data.py insert --path db/demo.csv --values=Dmitry,Moscow,+7
```

To insert another entry into the database:
```shell script
python3 apps/personal_data.py insert --path db/demo.csv --values=Alex,Vancouver,+1
```

Please note that only 3 specific columns (`name`, `address`, `phone_number`) are supported by the app.

### Display
To view the list of entries in `db/demo.csv` as a console-printed table:

```shell script
python3 apps/personal_data.py display --path db/demo.csv
# or
python3 apps/personal_data.py display --path db/demo.csv --format=table
```

To view the list of entries in `db/demo.csv` as an HTML table (opens in a default browser):

```shell script
python3 apps/personal_data.py display --path db/demo.csv --format=html
```

### Filter
To view all entries with `name=Dmitry` as a console-printed table:

```shell script
python3 apps/personal_data.py filter --path db/demo.csv --glob="name=Dmitry"
# or
python3 apps/personal_data.py filter --path db/demo.csv --glob="name=Dmitry" --display=table
```

To view same entries as HTML table:

```shell script
python3 apps/personal_data.py filter --path db/demo.csv --glob="name=Dmitry" --display=html
```

To view all entries containing `co` in its address as a console-printed table:

```shell script
python3 apps/personal_data.py filter --path db/demo.csv --glob="address=*co*"
```

### Convert
To convert a `CSV` file to a `JSON` file:

```shell script
python3 apps/personal_data.py convert --path db/demo.csv --converted_path db/demo.json
```

Now you can apply the same commands to `db/demo.json`:

```shell script
python3 apps/personal_data.py display --path db/demo.json
```

Note that currently only `CSV` and `JSON` formats are supported for both serialization and deserialization.
