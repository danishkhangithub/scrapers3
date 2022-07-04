# built-ins
# external
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
# internal
from config import DEFAULT_TIMEOUT

def decode_email(e):
    """Used for decoding protected email strings in press releases"""

    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e) - 1, 2):
        de += chr(int(e[i:i + 2], 16) ^ k)

    return de


class TimeoutHTTPAdapter(HTTPAdapter):
    """Custom class to incorporate timeout with retries in requests"""

    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def requests_retries():
    """Requests function with timeout and retries"""

    retries = Retry(total=3, backoff_factor=5,
                    status_forcelist=[429, 500, 502, 503, 504])
    adapter = TimeoutHTTPAdapter(max_retries=retries, timeout=20)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session
