#!/usr/bin/env python
"""Run migrations on Heroku and repair the known account/core history mismatch."""

import os
import sys
from pathlib import Path

import django
from django.core.management import call_command
from django.db import connections
from django.db import transaction
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.loader import MigrationLoader


def repair_history(connection):
    """Repair a database where account was recorded before the custom user app."""
    recorder = MigrationRecorder(connection)
    applied = set(recorder.applied_migrations())
    table_names = set(connection.introspection.table_names())

    account_initial = ("account", "0001_initial")
    core_initial = ("core", "0001_initial")

    if "core_user" not in table_names:
        print("Repairing migration history: applying core.0001_initial schema")
        loader = MigrationLoader(connection)
        migration = loader.get_migration(*core_initial)
        state = loader.project_state(migration.dependencies)
        with transaction.atomic(using=connection.alias):
            with connection.schema_editor() as schema_editor:
                migration.apply(state, schema_editor)
        if core_initial not in applied:
            recorder.record_applied(*core_initial)
        return True

    if account_initial in applied and core_initial not in applied:
        print("Repairing migration history: recording core.0001_initial")
        recorder.record_applied(*core_initial)
        return True

    core_0004 = ("core", "0004_class_is_archived_class_slug_class_updated_at")
    core_0004_columns = {"is_archived", "slug", "updated_at"}
    core_0004_index = "core_class_slug_e293aa55_like"

    if core_0004 not in applied and "core_class" in table_names:
        with connection.cursor() as cursor:
            description = connection.introspection.get_table_description(cursor, "core_class")
            existing_columns = {column.name for column in description}
            constraints = connection.introspection.get_constraints(cursor, "core_class")

        if core_0004_columns.issubset(existing_columns) and core_0004_index in constraints:
            print("Repairing migration history: recording core.0004_class_is_archived_class_slug_class_updated_at")
            recorder.record_applied(*core_0004)
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