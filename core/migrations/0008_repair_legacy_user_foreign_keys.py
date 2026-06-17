from django.db import migrations


def repair_legacy_user_foreign_keys(apps, schema_editor):
    connection = schema_editor.connection

    if connection.vendor != "postgresql":
        return

    User = apps.get_model("core", "User")
    user_table = User._meta.db_table

    qn = connection.ops.quote_name

    def table_exists(cursor, table_name):
        cursor.execute("SELECT to_regclass(%s)", [table_name])
        return cursor.fetchone()[0] is not None

    def truncate_identifier(identifier, max_len=63):
        if len(identifier) <= max_len:
            return identifier
        return identifier[:max_len]

    targets = [
        ("django_admin_log", "user_id"),
        ("account_emailaddress", "user_id"),
    ]

    with connection.cursor() as cursor:
        if not table_exists(cursor, user_table):
            return

        for table_name, column_name in targets:
            if not table_exists(cursor, table_name):
                continue

            cursor.execute(
                """
                SELECT con.conname, ref.relname
                FROM pg_constraint con
                JOIN pg_class rel ON rel.oid = con.conrelid
                JOIN pg_class ref ON ref.oid = con.confrelid
                JOIN pg_attribute att
                    ON att.attrelid = rel.oid
                    AND att.attnum = ANY(con.conkey)
                WHERE con.contype = 'f'
                    AND rel.relname = %s
                    AND att.attname = %s
                """,
                [table_name, column_name],
            )
            existing_constraints = cursor.fetchall()

            for constraint_name, referenced_table in existing_constraints:
                if referenced_table == user_table:
                    continue

                cursor.execute(
                    f"""
                    DELETE FROM {qn(table_name)} t
                    WHERE t.{qn(column_name)} IS NOT NULL
                        AND NOT EXISTS (
                            SELECT 1
                            FROM {qn(user_table)} u
                            WHERE u.id = t.{qn(column_name)}
                        )
                    """
                )

                cursor.execute(
                    f"ALTER TABLE {qn(table_name)} DROP CONSTRAINT IF EXISTS {qn(constraint_name)}"
                )

            cursor.execute(
                """
                SELECT 1
                FROM pg_constraint con
                JOIN pg_class rel ON rel.oid = con.conrelid
                JOIN pg_class ref ON ref.oid = con.confrelid
                JOIN pg_attribute att
                    ON att.attrelid = rel.oid
                    AND att.attnum = ANY(con.conkey)
                WHERE con.contype = 'f'
                    AND rel.relname = %s
                    AND att.attname = %s
                    AND ref.relname = %s
                LIMIT 1
                """,
                [table_name, column_name, user_table],
            )
            has_correct_fk = cursor.fetchone() is not None

            if not has_correct_fk:
                base_name = f"{table_name}_{column_name}_fk_{user_table}"
                constraint_name = truncate_identifier(base_name)
                cursor.execute(
                    f"""
                    ALTER TABLE {qn(table_name)}
                    ADD CONSTRAINT {qn(constraint_name)}
                    FOREIGN KEY ({qn(column_name)})
                    REFERENCES {qn(user_table)} (id)
                    DEFERRABLE INITIALLY DEFERRED
                    """
                )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_sync_user_emails"),
    ]

    operations = [
        migrations.RunPython(
            repair_legacy_user_foreign_keys,
            migrations.RunPython.noop,
        ),
    ]
