import os

from vinyl.lib.asset import resource
from vinyl.lib.connect import FileConnector


@resource
def local_filesystem():
    return FileConnector(path=os.path.join(os.path.dirname(__file__), "data"))
