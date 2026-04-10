# LogLensBlue – Analyse de logs SSH

Petit outil personnel permettant d’analyser les logs SSH (`/var/log/auth.log` ou tout fichier compatible) pour détecter les tentatives de connexion suspectes.  
Le but est de comprendre ce qui se passe sur une machine Linux, sans attaque ni scan autre que la lecture des logs existants.

## Fonctionnalités

- Lecture de fichiers de logs SSH (type `auth.log` de `sshd`).
- Détection :
  - de tentatives de brute‑force SSH (multiples échecs de mot de passe depuis la même IP),
  - de connexions effectuées en tant que `root`.
- Stockage structuré dans une base de données SQLite (`logs.db`).
- Affichage terminal moderne avec couleurs, tableaux et statistiques globales :
  - comptage d’événements et d’alertes,
  - répartition par niveau de risque,
  - top IP les plus actives.

Tout reste **100 % local** : l’outil ne communique avec aucun serveur externe, il se contente de lire et d’analyser des fichiers déjà présents sur la machine.

## Prérequis

- Python 3.9+  
- Un environnement virtuel (recommandé)  
- `rich` (installé depuis le venv) :

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install rich
```

## Installation rapide

Depuis le dossier du projet :

```bash
cd ~/LogLensBlue
```

### 1. (Si tu n’as pas déjà le venv)

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install rich
```

### 2. Lancer l’analyse

Le script peut lire soit un fichier de test, soit vos logs système :

```bash
cd ~/LogLensBlue
source venv/bin/activate
PYTHONPATH=. python -m src.main
```

Par défaut, `src/main.py` analyse le fichier de test :

```python
path = "/home/sonny/LogLensBlue/sample_logs/auth.log"
```

Pour lire vos logs système, modifie cette ligne dans `src/main.py` :

```python
path = "/var/log/auth.log"
```

## Architecture

- `src/parser.py`  
  - parseur simple pour lignes `sshd` (`Failed password`, `Accepted password`).
  - exporte une fonction `parse_auth_log(path: str) -> list[dict]`.

- `src/rules_engine.py`  
  - moteur de règles :
    - `SSH_BRUTE_SIMPLE` (bruteforce SSH),
    - `SSH_ROOT_LOGIN` (connexion root).

- `src/models.py`  
  - classes `Event` et `Alert` pour structurer les données.

- `src/db.py`  
  - création + alimentation d’une base SQLite (`events`, `alerts`).

- `src/main.py`  
  - orchestre le tout + affichage Rich :  
    - rapport d’analyses,  
    - tableau d’alertes,  
    - statistiques globales (top IP, niveaux d’alertes, etc.).

## Exemple de sortie

```text
⚓ LogLens Blue — Analyse de logs SSH (mode B+)

📄 3 lignes SSH lues dans: /home/sonny/LogLensBlue/sample_logs/auth.log

🚨 [MEDIUM] SSH_BRUTE_SIMPLE
   ├─ IP:        192.0.2.1
   └─ ...

🚨 [HIGH] SSH_ROOT_LOGIN
   ├─ IP:        192.0.2.1
   └─ ...

✅ Résumé de l'analyse
   ├─ 3 événements analysés
   └─ 3 alertes générées

📊 Statistiques globales
   📄 3 événements analysés
   🚨 3 alertes générées
   📍 Répartition par niveau : MEDIUM (2), HIGH (1)
   🌍 Top IP : 192.0.2.1 → 3

🗂️ Résumé des alertes SSH
IP          Utilisateur        Règle            Niveau
----------  -----------------  ---------------  --------
192.0.2.1   invalid user admin SSH_BRUTE_SIMPLE MEDIUM
192.0.2.1   root               SSH_ROOT_LOGIN   HIGH
```

## Pourquoi ce projet ?

Ce projet est une petite expérience personnelle d’analyse de logs SSH, développée pour :
- pratiquer la lecture de fichiers logs système,
- créer un moteur de règles simple,
- améliorer l’affichage terminal avec `rich`,
- garder une visibilité propre et lisible sur les activités SSH sans dépendre d’outils maison complexes.

Il n’a pas vocation à remplacer des SIEM ou outils DFIR professionnels, mais plutôt à servir d’outil didactique et d’illustration concrète lors de projets de sécurité ou de cybersécurité.

## Licence

Le projet est proposé à titre informatif et didactique, sans garantie.

---

Nous pouvons toujours étendre LogLensBlue vers :
- un dashboard web,  
- l’ajout de nouvelles règles (fail2ban, scans de ports, etc.),  
- la prise en charge de différents formats de logs.

Mais pour l’instant, la version actuelle est suffisante pour illustrer l’idée, sans chercher à faire plus compliqué que nécessaire.


