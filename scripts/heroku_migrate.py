#!/usr/bin/env python
"""Run migrations on Heroku and repair the known account/core history mismatch."""

import os
import sys
from pathlib import Path

import django
from django.core.management import call_command
from django.db import connections
from django.db.migrations.recorder import MigrationRecorder


def repair_history(connection):
    """Fake core initial if allauth account was recorded before the custom user app."""
    recorder = MigrationRecorder(connection)
    applied = set(recorder.applied_migrations())

    account_initial = ("account", "0001_initial")
    core_initial = ("core", "0001_initial")

    if account_initial in applied and core_initial not in applied:
        print("Repairing migration history: faking core.0001_initial")
        call_command("migrate", "core", "0001_initial", fake=True, verbosity=1)
        return True

    return False


def main():
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()

    connection = connections["default"]
    repair_history(connection)

    print("Running Django migrations...")
    call_command("migrate", verbosity=2)
    print("Migrations completed successfully.")


if __name__ == "__main__":
    main()