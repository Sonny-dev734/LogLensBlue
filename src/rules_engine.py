# src/rules_engine.py

from typing import Optional, List, Dict
import uuid
from src.models import Alert


def detect_ssh_brute(event: Dict[str, str]) -> Optional[Alert]:
    if event.get("log_type") != "ssh":
        return None

    if "Failed password" in event.get("message", "") or "Failed publickey" in event.get("message", ""):
        hint = (
            "Ceci ressemble à une tentative de brute‑force SSH : "
            "beaucoup de mots de passe erronés depuis une même IP. "
            "Vérifiez l’IP et si elle a le droit de se connecter."
        )

        return Alert(
            id=str(uuid.uuid4()),
            event_id="placeholder",
            rule_name="SSH_BRUTE_SIMPLE",
            level="MEDIUM",
            category="SSH",
            title="Tentative de brute‑force SSH",
            ip=event.get("ip"),
            user=event.get("user"),
            timestamp=event.get("ts"),
            hint=hint,
            tags=["bruteforce", "ssh", "high_risk"],
        )

    return None


def detect_ssh_root_login(event: Dict[str, str]) -> Optional[Alert]:
    if event.get("log_type") != "ssh":
        return None

    if "Accepted password for root" in event.get("message", ""):
        hint = (
            "Ceci est une connexion SSH en tant que root. "
            "Cette pratique est très sensible et souvent déconseillée. "
            "Vérifiez si cette connexion est autorisée et venait d’une IP connue."
        )

        return Alert(
            id=str(uuid.uuid4()),
            event_id="placeholder",
            rule_name="SSH_ROOT_LOGIN",
            level="HIGH",
            category="SSH",
            title="Connexion SSH en root détectée",
            ip=event.get("ip"),
            user=event.get("user"),
            timestamp=event.get("ts"),
            hint=hint,
            tags=["root_login", "ssh", "critical"],
        )

    if "Accepted publickey for root" in event.get("message", ""):
        hint = (
            "Ceci est une connexion SSH en tant que root via clé publique. "
            "Même via clé publique, les connexions root restent très sensibles. "
            "Vérifiez si cette connexion est autorisée."
        )

        return Alert(
            id=str(uuid.uuid4()),
            event_id="placeholder",
            rule_name="SSH_ROOT_LOGIN",
            level="HIGH",
            category="SSH",
            title="Connexion SSH root (clé publique) détectée",
            ip=event.get("ip"),
            user=event.get("user"),
            timestamp=event.get("ts"),
            hint=hint,
            tags=["root_login", "ssh", "critical"],
        )

    return None


class RulesEngine:
    def __init__(self):
        pass

    def detect_alerts(self, events: List[Dict[str, str]]) -> List[Alert]:
        alerts: List[Alert] = []

        for event in events:
            alert_brute = detect_ssh_brute(event)
            if alert_brute:
                alerts.append(alert_brute)

            alert_root = detect_ssh_root_login(event)
            if alert_root:
                alerts.append(alert_root)

        return alerts





