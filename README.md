# Simple data storage library

## About the project

The repository provides a simple yet extensible library and a console app for storing uniform data in multiple formats.

The library has the following features:
* The basic in-memory **data storage** with insertion capabilities is provided, although more sophisticated storage types, such as databases, can be added naturally.
* JSON and CSV **serialisation** formats are provided out-of-the box, although it is straightforward to implement other formats.
* Data **filtering** using a simple glob syntax is supported, but other filter types can be added.

The code is written in Python 3.7 using only standard libraries.

## Quick Start

If you are interested in a console app implementing the key library features, please refer to the [app manual](docs/APP_MANUAL.md).

To get an overview of the library structure and how to use and extend it please read the [library tutorial](docs/LIBRARY_TUTORIAL.md).

## Project structure

* `apps` - applications that use the developed library
* `docs` - detailed documentation for the library and application
* `db` - folder containing sample database files
* `src` - the main library code
* `samples` - sample code to get familiar with the library
* `tests` - tests for the library

## What could be improved
* A better way of adding new classes to factories without manually altering name-class dictionaries and with automatic search paths setting via environment variables
* Logging
* Error handling (we often get not very user-friendly errors)
* Thread safety