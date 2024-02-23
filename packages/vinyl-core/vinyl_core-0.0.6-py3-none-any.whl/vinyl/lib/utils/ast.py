import ast
import os
import re


class ClassInfo:
    def __init__(self, name, excluded_attributes=[]):
        self.name = name
        self.excluded_attrs = excluded_attributes
        self.attributes_dict = {}

    def add_attribute(self, key, value):
        if key not in self.excluded_attrs:
            self.attributes_dict[key] = value


class ClassFinder(ast.NodeVisitor):
    def __init__(self, excluded_attributes=[]):
        self.classes = []
        self.excluded_attrs = excluded_attributes

    def visit_ClassDef(self, node):
        class_info = ClassInfo(node.name, self.excluded_attrs)

        # Look for assignments that occur directly in the class body
        for body_item in node.body:
            # Only handle type-annotated assignments with a value
            if isinstance(body_item, ast.AnnAssign) and body_item.value is not None:
                if isinstance(body_item.target, ast.Name):
                    # Add the attribute along with its value's AST
                    class_info.add_attribute(
                        body_item.target.id, ast.unparse(body_item.value)
                    )

        self.classes.append(class_info)
        self.generic_visit(node)  # Continue visiting child nodes


def find_classes_and_attributes(file_path):
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as file:
        source = file.read()

    tree = ast.parse(source)
    finder = ClassFinder(
        [
            "_table",
            "_unique_name",
            "_path",
            "_twin_path",
            "_row_count",
            "_schema",
            "_database",
        ]
    )
    finder.visit(tree)

    return finder.classes[0].attributes_dict


# more accurate
def get_imports_from_file_ast(file_path):
    with open(file_path, "r") as file:
        source = file.read()

    imports = ""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += ast.unparse(node)
        elif isinstance(node, ast.ImportFrom):
            imports += ast.unparse(node)
        elif isinstance(node, ast.ClassDef):
            break
        imports += "\n"

    return imports


# more literal
def get_imports_from_file_regex(file_path, regex="@source"):
    with open(file_path, "r") as file:
        source = file.read()

    parts = re.split(regex, source, re.MULTILINE)

    if len(parts) == 1:
        return ""

    return parts[0]
