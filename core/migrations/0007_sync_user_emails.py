from django.db import migrations

from allauth.account.models import EmailAddress


def sync_user_emails(apps, schema_editor):
    User = apps.get_model("core", "User")

    for user in User.objects.all().iterator():
        user_email = (user.email or "").strip()
        email_addresses = EmailAddress.objects.filter(user_id=user.pk)

        if user_email:
            EmailAddress.objects.update_or_create(
                user_id=user.pk,
                email=user_email,
                defaults={
                    "primary": True,
                    "verified": False,
                },
            )
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
