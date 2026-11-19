import httpx

class RequestEngine:
    def __init__(self, timeout: float = 8.0, user_agent: str = "SQLSentinel/1.0 (authorized-audint)"):
        self.client = httpx.Client(
            timeout=httpx.Timeout(timeout),
            follow_redirects=False,
            headers={"User-Agent": user_agent, "Accept": "text/html, application/json;q=0.9, */*;q=0.5"},
            limits=httpx.Limits(max_connections=1, max_keepalive_connections=1),
        )

    def get(self, url: str):
        return self.client.get(url)

    def close(self):
        self.client.close()
        