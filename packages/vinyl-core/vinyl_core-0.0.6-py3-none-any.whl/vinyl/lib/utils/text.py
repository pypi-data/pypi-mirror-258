import random
import re
import string
from urllib.parse import urlparse


def generate_random_ascii_string(length=30):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def split_interval_string(s):
    for i, char in enumerate(s):
        if not char.isdigit():
            return int(s[:i]), s[i:]
    return int(s), ""


def extract_uri_scheme(path):
    result = urlparse(path)
    return result.scheme


def make_python_identifier(str_):
    return re.sub(r"\W|^(?=\d)", "_", str_)
