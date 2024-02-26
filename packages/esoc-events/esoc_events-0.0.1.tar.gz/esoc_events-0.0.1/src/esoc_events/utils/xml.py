import re
from typing import Any


def replace_parenthesis(source: str) -> str:
    regex = r"\(([^\)]+)\)"
    subst = 'type="\\1"'
    return re.sub(regex, subst, source, count=0, flags=re.MULTILINE)


def replace_parenthesis_tags(path: Any) -> Any:
    with open(path) as non_xml_input:
        content = non_xml_input.read()
        return replace_parenthesis(content)
