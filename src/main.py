#!/usr/bin/env python3

import uuid
from typing import List, Dict, Counter
from src.models import Event, Alert
from src.parser import parse_auth_log
from src.rules_engine import RulesEngine
from src.db import init_db, save_event, save_alert
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

console = Console()
layout = Layout()


def analyze_event(event: Dict[str, str]) -> List[Alert]:
    engine = RulesEngine()
    rules_alerts = engine.detect_alerts([event])
    return rules_alerts


def summarize_alerts(alerts: List[Alert]):
    table = Table(title="🗂️ Résumé des alertes SSH", show_header=True, header_style="bold magenta")
    table.add_column("IP", style="cyan")
    table.add_column("Utilisateur", style="green")
    table.add_column("Règle", style="yellow")
    table.add_column("Niveau", style="red")

    for alert in alerts:
        table.add_row(alert.ip, alert.user, alert.rule_name, alert.level)

    console.print(table)


def build_stats_panel(alerts: List[Alert], events: List[Dict[str, str]]):
    stats_text = Text()

    # Stat 1: nombre d’événements
    stats_text.append("📄 ")
    stats_text.append("Événements analysés: ", style="blue")
    stats_text.append(f"{len(events)}\n", style="bold blue")

    # Stat 2: nombre d’alertes
    stats_text.append("🚨 ")
    stats_text.append("Alertes générées: ", style="red")
    stats_text.append(f"{len(alerts)}\n", style="bold red")

    # Stat 3: répartition par niveau
    levels = Counter(alert.level for alert in alerts)
    stats_text.append("📍 Répartition par niveau:\n", style="green")
    for level, count in levels.items():
        stats_text.append(f"  {level}: {count}\n", style="green")

    # Stat 4: top IP
    ips = Counter(alert.ip for alert in alerts if alert.ip)
    if ips:
        stats_text.append("🌍 Top IP concernées:\n", style="magenta")
        for ip, count in ips.most_common(3):
            stats_text.append(f"  {ip} → {count}\n", style="magenta")
    else:
        stats_text.append("🌍 Aucune IP identifiée pour les alertes.\n", style="magenta")

    panel = Panel(stats_text, title="📊 Statistiques globales", border_style="blue")
    console.print(panel)


def main():
    console.print("\n" + "─" * 100, justify="center")
    console.print("⚓ LogLens Blue — Analyse de logs SSH (mode B+)", justify="center")
    console.print("─" * 100 + "\n", justify="center")

    # 1. Initialiser la base de données
    init_db()

    # 2. Choisir le fichier de logs
    #   → décommente UNE seule ligne
    # path = "/var/log/auth.log"                    # ton vrai fichier
    path = "/home/sonny/LogLensBlue/sample_logs/auth.log"  # fichier de test

    # 3. Parser le fichier
    events: List[Dict[str, str]] = parse_auth_log(path)
    console.print(f"📄 {len(events)} lignes SSH lues dans: {path}\n")

    # 4. Compter les événements et alertes
    total_analyzed = 0
    total_alerts = 0
    all_alerts: List[Alert] = []

    # 5. Analyser chaque événement
    for ev in events:
        e = Event(
            id=str(uuid.uuid4()),
            timestamp=ev.get("ts"),
            source="sshd",
            user=ev.get("user"),
            message=ev.get("message"),
            metadata=ev,
        )
        save_event(e)

        alerts = analyze_event(ev)
        for alert in alerts:
            total_alerts += 1
            all_alerts.append(alert)
            save_alert(alert)
            console.print(
                f"\n🚨 [{alert.level}] {alert.rule_name}\n"
                f"   ├─ IP:        {alert.ip}\n"
                f"   ├─ User:      {alert.user}\n"
                f"   ├─ Timestamp: {alert.timestamp}\n"
                f"   └─ Hint:      {alert.hint}"
            )

        total_analyzed += 1

    # 6. Résumé final + statistiques
    console.rule("[bold green]✅ Résumé de l'analyse[/bold green]")
    console.print(f"   ├─ {total_analyzed} événements analysés")
    console.print(f"   └─ {total_alerts} alertes générées\n")

    # 7. Panel de statistiques
    if events:
        build_stats_panel(all_alerts, events)

    # 8. Tableau des alertes
    if all_alerts:
        summarize_alerts(all_alerts)

    # 9. Section optionnelle future (notifications / webhook)
    # → désactivée par défaut
    # console.rule("[bold cyan]📡 Notifications optionnelles (B+)[/bold cyan]")
    # console.print("🔒 Toutes fonctions de notification restent désactivées par défaut.")
    # console.print("Vous pouvez ajouter un 'mock' de notification (ex. print) ici si besoin.")


if __name__ == "__main__":
    main()



