from typing import Dict, Optional, List, Tuple
from urllib.parse import unquote
from tennis_board.config import templates


def parse_request_form(data: str) -> Dict:
    data_kv = {}
    for kv in data.split("&"):
        key, value = kv.split("=")
        data_kv[key] = unquote(value)
    return data_kv


def not_found(path: str) -> bytes:
    template = templates.get_template("error.html")
    return template.render(title="error", message=f"Page '{path}' not found").encode()


def bad_request(message: str) -> bytes:
    template = templates.get_template("error.html")
    return template.render(title="error", message=f"Bad request: {message}").encode()


def generate_headers(message: bytes, headers: Optional[Dict] = None) -> List[Tuple]:
    add_header = []
    if headers:
        add_header = list(headers.items())
    return [
        ("Content-Type", "text/html; charset=utf8"),
        ("Content-Length", str(len(message))),
        *add_header,
    ]
