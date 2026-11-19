import pytest
from sqlsentinel.scope import validate_target, ScopeError

def test_local_target_requires_authorization():
    with pytest.raises(ScopeError):
        validate_target("http://127.0.0.1/x?id=1", "127.0.0.1", False)

def test_scope_host_must_match():
    with pytest.raises(ScopeError):
        validate_target("http://127.0.0.1/x?id=1", "localhost", True)

def test_localhost_allowed_with_ack():
    host, scheme = validate_target("http://127.0.0.1/x?id=1", "127.0.0.1", True)
    assert host == "127.0.0.1"
    assert scheme == "http"

def test_public_target_requires_flag():
    with pytest.raises(ScopeError):
        validate_target("https://example.com/?id=1", "example.com", True)
