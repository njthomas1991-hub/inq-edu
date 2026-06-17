from django.db import migrations


def sync_user_emails(apps, schema_editor):
    User = apps.get_model("core", "User")
    EmailAddress = apps.get_model("account", "EmailAddress")

    # First, delete orphaned EmailAddress records (user_id doesn't exist in User table).
    # Keep migration writes FK-safe across environments with legacy schema drift.
    valid_user_ids = set(User.objects.values_list("pk", flat=True))
    orphaned = EmailAddress.objects.exclude(user_id__in=valid_user_ids)
    orphaned.delete()

    # Backfill only User.email from primary EmailAddress when User.email is blank.
    # Avoid creating/updating EmailAddress rows inside migration to prevent FK issues.
    for user in User.objects.all().iterator():
        user_email = (user.email or "").strip()
        email_addresses = EmailAddress.objects.filter(user_id=user.pk)

        if user_email:
            continue

        primary_email_address = (
            email_addresses.filter(primary=True).order_by("id").first()
            or email_addresses.order_by("id").first()
        )

        if primary_email_address and primary_email_address.email:
            user.email = primary_email_address.email
            user.save(update_fields=["email"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_create_default_admin_user"),
    ]

    operations = [
        migrations.RunPython(sync_user_emails, migrations.RunPython.noop),
    ]
