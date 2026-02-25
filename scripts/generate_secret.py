#!/usr/bin/env python3
"""Generate a secure Django SECRET_KEY for local use.

Usage:
    python scripts/generate_secret.py

Copy the output into your local .env file as:
    DJANGO_SECRET_KEY=the_generated_value

Note: Do NOT commit your .env file to version control.
"""

import secrets


def main():
    key = secrets.token_urlsafe(50)
    print(key)


if __name__ == "__main__":
    main()
