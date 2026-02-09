#!/usr/bin/env python
"""
Demo: Using Pillow to create cute fuzzy monster avatars
Shows various ways to generate adorable monsters
"""

from cute_monster_avatar import (
    create_monster_avatar,
    create_multiple_monsters,
    save_avatar_to_file
)


def demo_basic_avatar():
    """Create a basic cute monster avatar."""
    print("=" * 60)
    print("1️⃣  BASIC CUTE MONSTER AVATAR")
    print("=" * 60)
    
    # Simple one-liner to create a monster
    monster = create_monster_avatar()
    print("✓ Created PIL Image object")
    print(f"  Size: {monster.size}")
    print(f"  Format: {monster.format}")
    
    monster.save('demo_basic.png')
    print("✓ Saved as demo_basic.png\n")


def demo_custom_colors():
    """Create monsters with custom colors."""
    print("=" * 60)
    print("2️⃣  CUSTOM COLOR MONSTERS")
    print("=" * 60)
    
    # Pink fuzzy monster with blue eyes
    pink_monster = create_monster_avatar(
        body_color='#FF6B9D',
        eye_color='#4A90E2',
        mouth_color='#FF6F61'
    )
    print("✓ Pink monster with blue eyes")
    pink_monster.save('demo_pink.png')
    
    # Purple with star eyes effect
    purple_monster = create_monster_avatar(
        body_color='#6C5CE7',
        eye_color='#000000',
        mouth_color='#FFB347'
    )
    print("✓ Purple monster with orange mouth")
    purple_monster.save('demo_purple.png')
    
    # Cyan cheerful monster
    cyan_monster = create_monster_avatar(
        body_color='#00D2FF',
        eye_color='#FF6B9D',
        mouth_color='#50C878'
    )
    print("✓ Cyan monster with pink eyes")
    cyan_monster.save('demo_cyan.png')
    print()


def demo_different_sizes():
    """Create monsters at different sizes."""
    print("=" * 60)
    print("3️⃣  DIFFERENT SIZES")
    print("=" * 60)
    
    sizes = [100, 200, 300, 500]
    for size in sizes:
        monster = create_monster_avatar(size=size)
        filename = f'demo_size_{size}.png'
        monster.save(filename)
        print(f"✓ {size}px monster saved as {filename}")
    print()


def demo_base64_output():
    """Create avatar as base64 (useful for web)."""
    print("=" * 60)
    print("4️⃣  BASE64 FOR WEB EMBEDDING")
    print("=" * 60)
    
    # Get base64 string (embed in HTML)
    b64_str = create_monster_avatar(
        body_color='#FF6B9D',
        output_format='base64'
    )
    
    print("✓ Generated base64 string (first 100 chars):")
    print(f"  {b64_str[:100]}...")
    print(f"\n  Use in HTML as:")
    print(f"  <img src=\"data:image/png;base64,{b64_str[:50]}...\" />")
    print()


def demo_batch_generation():
    """Generate multiple random monsters."""
    print("=" * 60)
    print("5️⃣  BATCH GENERATION")
    print("=" * 60)
    
    monsters = create_multiple_monsters(count=6, size=200)
    print(f"✓ Generated {len(monsters)} random monsters")
    
    # Combine into a grid (optional)
    from PIL import Image
    
    # Create a 2x3 grid
    grid = Image.new('RGB', (600, 400), color='#F0F8FF')
    positions = [
        (0, 0), (200, 0), (400, 0),
        (0, 200), (200, 200), (400, 200)
    ]
    
    for i, (monster, pos) in enumerate(zip(monsters, positions)):
        grid.paste(monster, pos)
    
    grid.save('demo_grid.png')
    print("✓ Created monster grid in demo_grid.png\n")


def demo_color_palette():
    """Show the cute color palette used."""
    print("=" * 60)
    print("6️⃣  CUTE COLOR PALETTE")
    print("=" * 60)
    
    palette = [
        '#FF6B9D',  # Pink
        '#C44569',  # Deep pink
        '#4A90E2',  # Blue
        '#50C878',  # Emerald
        '#FFB347',  # Orange
        '#B39DDB',  # Purple
        '#FF6F61',  # Coral
        '#6C5CE7',  # Lavender
        '#00D2FF',  # Cyan
        '#FFA500',  # Gold
    ]
    
    print("Available colors for cute monsters:")
    for color in palette:
        print(f"  {color}")
    print()


def demo_usage_examples():
    """Show code examples."""
    print("=" * 60)
    print("7️⃣  USAGE EXAMPLES")
    print("=" * 60)
    
    examples = """
    # Basic usage
    monster = create_monster_avatar()
    monster.show()  # Display
    monster.save('my_monster.png')  # Save
    
    # Custom colors
    monster = create_monster_avatar(
        body_color='#FF6B9D',      # Pink body
        eye_color='#000000',        # Black eyes
        mouth_color='#FF6F61'       # Coral mouth
    )
    
    # Different sizes
    small = create_monster_avatar(size=100)
    medium = create_monster_avatar(size=300)
    large = create_monster_avatar(size=600)
    
    # For web (base64)
    base64_img = create_monster_avatar(
        body_color='#FF6B9D',
        output_format='base64'
    )
    html = f'<img src="data:image/png;base64,{base64_img}" />'
    
    # For APIs (bytes)
    png_bytes = create_monster_avatar(
        body_color='#00D2FF',
        output_format='bytes'
    )
    response = HttpResponse(png_bytes, content_type='image/png')
    
    # Multiple monsters
    monsters = create_multiple_monsters(count=10)
    for i, monster in enumerate(monsters):
        monster.save(f'monster_{i}.png')
    
    # Direct file save
    save_avatar_to_file(
        'avatar.png',
        size=300,
        body_color='#FF6B9D',
        eye_color='#4A90E2',
        mouth_color='#FF6F61'
    )
    """
    
    print(examples)


if __name__ == '__main__':
    print("\n")
    print("🎨" * 30)
    print("  CUTE FUZZY MONSTER AVATAR GENERATOR DEMO")
    print("🎨" * 30)
    print()
    
    # Run all demos
    demo_basic_avatar()
    demo_custom_colors()
    demo_different_sizes()
    demo_base64_output()
    demo_batch_generation()
    demo_color_palette()
    demo_usage_examples()
    
    print("=" * 60)
    print("✨ Demo complete! Check generated PNG files.")
    print("=" * 60)
    print()
