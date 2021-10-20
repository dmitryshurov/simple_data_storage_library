from ds_simple_db.core.factory import Factory
from .html_display import HTMLDisplay
from .table_display import TableDisplay


class DisplayFactory(Factory):
    """
    A factory to create serializers
    """
    classes = dict(
        html=HTMLDisplay,
        table=TableDisplay
    )
