import ipaddress
from urllib.parse import urlparse

class ScopeError(ValueError):
    pass

def validate_target(url: str, scope_host: str, authorized: bool,
                    allow_public: bool = False) -> tuple[str, str]:
    if not authorized:
        raise ScopeError("Active scanning requires --authorized.")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ScopeError("Target must be an absolute http:// or https:// URL.")
    host = parsed.hostname.lower().rstrip(".")
    expected = scope_host.lower().rstrip(".")
    if host != expected:
        raise ScopeError(f"Target host {host!r} does not exactly match --scope-host {expected!r}.")
    if parsed.username or parsed.password:
        raise ScopeError("Credentials embedded in URLs are not permitted.")
    try:
        ip = ipaddress.ip_address(host)
        is_private = ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        is_private = host == "localhost" or host.endswith(".localhost") or host.endswith(".test")
    if not is_private and not allow_public:
        raise ScopeError("Public target blocked. Add --allow-public-target only with written authorization.")
    return host, parsed.scheme
