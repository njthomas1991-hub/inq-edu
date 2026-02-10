#!/usr/bin/env python
"""Check Avatar table structure"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), 'env.py')
if os.path.isfile(env_path):
    with open(env_path) as f:
        exec(f.read())

django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Check if table exists
    cursor.execute("""
        SELECT EXISTS(
            SELECT 1 FROM information_schema.tables 
            WHERE table_name='core_avatar'
        );
    """)
    exists = cursor.fetchone()[0]
    
    if exists:
        print("✓ Avatar table EXISTS")
        # Get columns
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name='core_avatar'
            ORDER BY ordinal_position;
        """)
        print("\nColumns in core_avatar:")
        for col, dtype in cursor.fetchall():
            print(f"  - {col} ({dtype})")
    else:
        print("✗ Avatar table DOES NOT EXIST - recreating now...")
        # Recreate it
        cursor.execute("""
            CREATE TABLE core_avatar (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL UNIQUE,
                body_type VARCHAR(20) DEFAULT 'round_blue',
                eye_type VARCHAR(20) DEFAULT 'big_happy',
                mouth_type VARCHAR(20) DEFAULT 'smile',
                accessory VARCHAR(20) DEFAULT 'none',
                primary_color VARCHAR(7) DEFAULT '#FF6B9D',
                accent_color VARCHAR(7) DEFAULT '#FFB347',
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                FOREIGN KEY (user_id) REFERENCES core_user(id)
            );
        """)
        print("✓ Avatar table created successfully")
        connection.commit()
