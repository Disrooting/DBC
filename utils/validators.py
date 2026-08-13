import re
from pathlib import Path


def valid_token(token: str) -> bool:
    return len(token.strip()) > 30


def valid_invite(link: str):

    pattern = r"(?:discord\.gg/|discord\.com/invite/)([A-Za-z0-9_-]+)"

    match = re.search(pattern, link)

    if match:
        return match.group(1)

    return None


def valid_file(path):

    return Path(path).exists()