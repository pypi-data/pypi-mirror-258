from dataclasses import dataclass
import os
from abc import ABC, abstractmethod



class Source:
    name: str
    path: str

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    @property
    def tables(self):
        source_tables = [
            SourceTable(
                name=item,
                type="parquet",
                path=os.path.join(self.path, item, "data"),
            )
            for item in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, item))
        ]
        source_tables_with_data = []
        for table in source_tables:
            if os.path.exists(table.path) and any(
                file.endswith(".parquet") for file in os.listdir(table.path)
            ):
                source_tables_with_data.append(table)
        # for now we want to filter any source table that isn't actually back by a parquet file
        return source_tables_with_data


@dataclass
class SourceTable:
    name: str
    type: str
    path: str


class SourceRepository(ABC):
    @abstractmethod
    def get_sources(self) -> list[Source]:
        pass
