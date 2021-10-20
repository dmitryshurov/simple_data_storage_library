import os
import tempfile
import webbrowser
from typing import List

from ds_simple_db.core.entry import Entry
from ds_simple_db.serializers.html_serializer import HTMLSerializer
from personal_data.display.display_base import Display


class HTMLDisplay(Display):
    def display(self, entries: List[Entry]):
        path = os.path.join(tempfile.mkdtemp(), 'data_storage.html')

        html = HTMLSerializer().entries_to_string(entries)

        with open(path, 'w') as fp:
            fp.write(html)

        webbrowser.open('file://' + os.path.realpath(path))
