#!/usr/bin/env python
"""
Simple test script for the monster avatar generator
Run from project root: python test_avatar_generator.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Import after Django setup
from core.avatar_generator import create_monster_avatar, get_random_avatar_data

# Test the function
print("🎨 Testing Monster Avatar Generator\n")
print("=" * 50)

# Generate a cute fuzzy monster with random colors, big eyes, and a smile
print("\n✨ Generating cute fuzzy monster avatar...")
avatar = create_monster_avatar(user=None, cute_bias=True)

print(f"""
🦄 Your Cute Monster:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Body:       {avatar.body_shape.upper()} shape
  Color:      {avatar.body_color}
  
  Arms:       {avatar.arm_style} style ({avatar.arm_color})
  Legs:       {avatar.leg_style} ({avatar.leg_color})
  
  Eyes:       {avatar.eye_style.upper()} 👀 ({avatar.eye_color})
  Mouth:      {avatar.mouth_style.upper()} 😊 ({avatar.mouth_color})
  Teeth:      {'Yes ✓' if avatar.has_teeth else 'No ✗'}
  
  Accessories:
    👓 Glasses:   {'Yes ✓' if avatar.has_glasses else 'No ✗'}
    🦻 Ears:      {'Yes ✓' if avatar.has_ears else 'No ✗'}
    📡 Antennae:  {'Yes ✓' if avatar.has_antennae else 'No ✗'}
    👟 Shoes:     {'Yes ✓ (' + avatar.shoe_color + ')' if avatar.has_shoes else 'No ✗'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("\n🎲 Generating 5 more random monsters...")
print("=" * 50)

for i in range(5):
    monster = create_monster_avatar(user=None, cute_bias=True)
    accessories = []
    if monster.has_glasses:
        accessories.append("👓")
    if monster.has_ears:
        accessories.append("🦻")
    if monster.has_antennae:
        accessories.append("📡")
    if monster.has_shoes:
        accessories.append("👟")
    
    acc_str = " ".join(accessories) if accessories else "no accessories"
    
    print(f"{i+1}. {monster.body_shape.capitalize()} {monster.body_color} body, "
          f"{monster.eye_style} eyes, {monster.mouth_style} mouth, {acc_str}")

print("\n" + "=" * 50)
print("✅ Test complete! All monsters generated successfully.")
print("\nAPI Endpoints available:")
print("  GET  /avatar/generate/      - Get random avatar data (JSON)")
print("  POST /avatar/auto-generate/ - Auto-generate & save for current user")
print("  POST /avatar/save/          - Save custom avatar configuration")
