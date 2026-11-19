import httpx
import respx
from sqlsentinel.scanner import Scanner

@respx.mock
def test_scan_sends_bounded_requests():
    route = respx.get("http://127.0.0.1/item").mock(
        return_value=httpx.Response(200, text="<html>item found</html>")
    )
    scanner = Scanner(max_requests=3, delay=0.5)
    report = scanner.scan("http://127.0.0.1/item?id=1", "127.0.0.1")
    assert report.requests_sent <= 3
    assert report.parameters_tested == ["id"]
