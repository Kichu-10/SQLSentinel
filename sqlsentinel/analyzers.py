import re
from difflib import SequenceMatcher

DB_ERRORS = {
    "MySQL": [r"you have an error in your sql syntax", r"mysql_fetch", r"mysqli?_"],
    "PostgreSQL": [r"postgresql.*error", r"pg_query\(", r"unterminated quoted string"],
    "Microsoft SQL Server": [r"unclosed quotation mark", r"microsoft ole dc provider for sql server", r"sqlserver"],
    "SQLite": [r"sqlite error", r"sqlite3\.operationalerror", r"near .+ syntax error"],
    "Oracle": [r"ora-\d{4,5}", r"oracle error"],
}
WAF_MARKERS = ["access denied", "request blocked", "web application firewall",
               "cloudflare ray id", "incident id", "forbidden"]

def detect_db_errors(text: str) -> list[str]:
    low = text.lower()
    return [db for db, patterns in DB_ERRORS.items()
            if any(re.search(pattern, low, re.I) for pattern in patterns)]

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, re.sub(r"\s+", " ", a)[:20000],
                           re.sub(r"\s+", " ", b)[:20000]).ratio()

def detect_waf(status: int, text: str) -> bool:
    low = text.lower()
    return status in (401, 403, 406, 429, 503) or any(x in low for x in WAF_MARKERS)
