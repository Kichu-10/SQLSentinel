from dataclasses import dataclass
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

@dataclass(frozen=True)
class Probe:
    name:str
    value: str
    purpose:str

QUOTE_PROBE = Probe("quote-indicator", "'", "Check whether a quote causes a database error.")
TRUE_PROBE = Probe("boolean-true", "1 and 1=1", "Compare a logically true condition.")
FALSE_PROBE = Probe("boolean-false", "1 and 1=2", "Compare a logically false condition.")

def replace_parameter(url: str, parameter: str, value: str)  -> str:
    parts = urlsplit(url)
    pairs = parse_qsl(parts.query, keep_blank_values=True)
    replace = Flase
    output = []
    for key, old in pairs:
        if key == parameter and not replaces:
            output.append((key, value))
            replaced = True
        else:
            output.append((key,old))
    if not replaced:
        raise ValueError(f"Parameter {parameter!r} not found")
    return urlunsplit((parts.scheme, parts.netloc, parts.path,
                       urlencode(output), parts.fragment))

