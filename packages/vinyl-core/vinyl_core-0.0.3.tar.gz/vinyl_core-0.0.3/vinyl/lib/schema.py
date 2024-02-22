from ibis import Schema

from vinyl.lib.utils.graphics import print_schema


class VinylSchema:
    schema: Schema

    def __init__(self, schema: Schema):
        self.schema = schema

    def __str__(self):
        return self.schema.__str__().replace("ibis.Schema {", "vinyl.Schema {")

    def __repr__(self):
        return self.schema.__repr__().replace("ibis.Schema {", "vinyl.Schema {")

    def items(self):
        return self.schema.items()

    @property
    def names(self):
        return self.schema.names

    @property
    def types(self):
        return self.schema.types

    def __rich__(self):
        return print_schema(self.schema)
