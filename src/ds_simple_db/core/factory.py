from typing import List


class Factory:
    """
    The base class for all factories in the project.

    All you need to do in a subclass is fill the `classes` dict with the classes to be instantiated.
    """

    # TODO Add environment variable with paths to modules where to search for classes

    classes = dict()
    """
    A dictionary containing key-value pairs to retrieve classes by their string representation
    
    Example:
        classes = dict(
            csv_serializer=CSVSerializer,
            json_serializer=JSONSerializer
        )
    """

    @classmethod
    def list(cls) -> List[str]:
        """
        Get a list of registered classes

        :return: A list of registered class names
        """
        return list(cls.classes.keys())

    @classmethod
    def create(cls, class_name, *args, **kwargs):
        """
        Instantiate a class by its name and arguments

        :param class_name: A class string name (must be one of the keys registered in `classes` dict)
        :param args: Positional arguments to pass to an instance constructor
        :param kwargs: Keyword arguments to pass to an instance constructor
        :return: An created instance of a given class with given arguments
        """

        if class_name not in cls.classes:
            raise ValueError(f'Class `{class_name}` is not registered in a factory. Available names are {list(cls.classes.keys())}')

        Class = cls.classes[class_name]
        return Class(*args, **kwargs)
