from typing import List

from ds_simple_db.core.entry import Entry
from ds_simple_db.serializers.table_serializer import TableSerializer
from personal_data.display.display_base import Display


class TableDisplay(Display):
    def display(self, entries: List[Entry]):
        print('\n', TableSerializer().entries_to_string(entries), sep='')
