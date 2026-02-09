"""
Demo script showing how to use the monster avatar generator
Run this from the backend directory with: python manage.py shell < demo_avatar.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from backend.core.avatar_generator import create_monster_avatar, get_random_avatar_data
from django.contrib.auth.models import User

def demo_avatar_generation():
    """Demonstrate avatar generation"""
    
    print("=" * 60)
    print("🎨 Monster Avatar Generator Demo")
    print("=" * 60)
    
    # Example 1: Generate random avatar data (no user)
    print("\n1️⃣  Generating cute fuzzy monster avatar data...")
    avatar_data = get_random_avatar_data()
    print(f"   Body: {avatar_data['body_shape']} - {avatar_data['body_color']}")
    print(f"   Arms: {avatar_data['arm_style']} - {avatar_data['arm_color']}")
    print(f"   Legs: {avatar_data['leg_style']} - {avatar_data['leg_color']}")
    print(f"   Eyes: {avatar_data['eye_style']} - {avatar_data['eye_color']}")
    print(f"   Mouth: {avatar_data['mouth_style']} - {avatar_data['mouth_color']}")
    print(f"   Features: ", end="")
    features = []
    if avatar_data['has_teeth']:
        features.append("teeth")
    if avatar_data['has_glasses']:
        features.append("glasses")
    if avatar_data['has_ears']:
        features.append("ears")
    if avatar_data['has_antennae']:
        features.append("antennae")
    if avatar_data['has_shoes']:
        features.append(f"shoes ({avatar_data['shoe_color']})")
    print(", ".join(features) if features else "none")
    
    # Example 2: Generate multiple avatars to show variety
    print("\n2️⃣  Generating 3 random cute monster variations...")
    for i in range(3):
        avatar = create_monster_avatar(user=None, cute_bias=True)
        print(f"\n   Monster #{i+1}:")
        print(f"      {avatar.body_shape.capitalize()} body in {avatar.body_color}")
        print(f"      {avatar.eye_style.capitalize()} eyes with {avatar.mouth_style} mouth")
        accessories = []
        if avatar.has_glasses:
            accessories.append("wearing glasses")
        if avatar.has_ears:
            accessories.append("fuzzy ears")
        if avatar.has_antennae:
            accessories.append("cute antennae")
        if accessories:
            print(f"      Accessories: {', '.join(accessories)}")
    
    # Example 3: Create avatar for a specific user (if admin exists)
    print("\n3️⃣  Creating avatar for admin user (if exists)...")
    try:
        admin_user = User.objects.get(username='admin')
        avatar = create_monster_avatar(user=admin_user, cute_bias=True)
        print(f"   ✅ Avatar created for {admin_user.username}!")
        print(f"   Details: {avatar.body_shape} body, {avatar.eye_style} eyes, {avatar.mouth_style} mouth")
    except User.DoesNotExist:
        print("   ℹ️  Admin user not found. Create a user first to test this feature.")
    
    print("\n" + "=" * 60)
    print("✨ Demo complete! Use these functions in your views:")
    print("   - create_monster_avatar(user, cute_bias=True)")
    print("   - get_random_avatar_data()")
    print("=" * 60)

if __name__ == '__main__':
    demo_avatar_generation()
