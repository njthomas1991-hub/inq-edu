import os
import sys

# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inclusive_quest_education.settings")
import django

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


def delete_all_users():
    count = User.objects.count()
    print(f"Deleting {count} user(s) from the database...")
    User.objects.all().delete()
    print("Deletion complete.")


def create_user(username, email, password, role=None):
    print(f"Creating user username={username} email={email} role={role}")
    user = User.objects.create_user(username=username, email=email, password=password)
    if role:
        try:
            user.role = role
        except Exception:
            pass
    user.save()
    print(f"Created user id={user.id} username={user.username}")
    return user


def main():
    # Read desired new user from environment variables
    new_username = os.environ.get("NEW_USERNAME")
    new_email = os.environ.get("NEW_EMAIL")
    new_password = os.environ.get("NEW_PASSWORD")
    new_role = os.environ.get("NEW_ROLE")

    if not (new_email):
        print("ERROR: NEW_EMAIL is required. Aborting.")
        return 2

    # Derive username if not provided
    if not new_username:
        new_username = new_email.split("@", 1)[0]
        new_username = "".join(ch for ch in new_username if ch.isalnum()) or "user"

    if not new_password:
        # generate a random password
        import secrets

        new_password = secrets.token_urlsafe(12)

    # Confirm
    print("About to delete all users and create one new user:")
    print(
        f"  username={new_username}\n  email={new_email}\n  role={new_role}\n  password=(hidden)\n"
    )
    proceed = os.environ.get("CONFIRM_RESET")
    if proceed != "1":
        print("Set environment variable CONFIRM_RESET=1 to confirm and run again.")
        return 1

    delete_all_users()
    create_user(new_username, new_email, new_password, new_role)
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
