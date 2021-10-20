from ds_simple_db.core.factory import Factory

from .csv_serializer import CSVSerializer
from .json_serializer import JSONSerializer


class SerializerFactory(Factory):
    """
    A factory to create serializers.

    HTMLSerializer and TableSerializer are not included because they do not implement deserialization at the moment
    """
    classes = dict(
        csv=CSVSerializer,
        json=JSONSerializer
    )
