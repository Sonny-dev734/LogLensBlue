#!/usr/bin/env python3

import os
import sqlite3


def get_project_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_db_path():
    return os.path.join(get_project_dir(), "logs.db")


def get_schema_path():
    return os.path.join(get_project_dir(), "src", "db_schema.sql")


def run_schema():
    db_path = get_db_path()
    schema_path = get_schema_path()

    # si le DB existe déjà, on le supprime et on le recrée proprement
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑 DB supprimé, fresh start.")

    print("🔧 Initialisation de la base de données...")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    with open(schema_path) as f:
        schema = f.read()

    cur.executescript(schema)
    conn.commit()
    conn.close()

    print("🎉 DB initialisée avec succès.")


if __name__ == "__main__":
    run_schema()



