# src/parser.py

import re
import datetime
from typing import List, Dict


class BaseParser:
    def can_handle(self, line: str) -> bool:
        raise NotImplementedError

    def parse(self, line: str) -> dict:
        raise NotImplementedError


class SSHParser(BaseParser):
    PATTERN = re.compile(
        r"(?P<time>\w{3}  \d+ \d+:\d+:\d+).*sshd\[\d+\]: (?P<kind>Failed|Accepted) password for (?P<user>.+?) from (?P<ip>\S+) "
    )

    def can_handle(self, line: str) -> bool:
        return "sshd" in line and (
            "Failed password" in line or "Accepted password" in line
        )

    def parse(self, line: str) -> dict:
        line = line.strip()
        m = self.PATTERN.search(line)
        if not m:
            return {}

        groups = m.groupdict()
        status = "failure" if "Failed" == groups["kind"] else "success"

        now = datetime.datetime.utcnow()
        ts = f"{now.year:04d}-01-01T{groups['time'].split(' ')[-1]}Z"

        return {
            "log_type": "ssh",
            "hostname": "localhost",
            "ts": ts,
            "ip": groups["ip"],
            "user": groups["user"],
            "status": status,
            "message": line,
            "additional_tags": ["ssh", "auth", "password_attempt"],
            "original_file": "auth.log",
        }


def parse_auth_log(path: str) -> List[dict]:
    parser = SSHParser()
    events = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if parser.can_handle(line):
                    ev = parser.parse(line)
                    if ev:
                        events.append(ev)
    except FileNotFoundError:
        print(f"Erreur: fichier {path} non trouvé.")
        return []

    return events






