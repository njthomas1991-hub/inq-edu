"""
Cute Fuzzy Monster Avatar Generator using Pillow
Creates adorable monster avatars with round bodies and big eyes
"""

from PIL import Image, ImageDraw, ImageFilter
import random
from io import BytesIO
import base64


def create_monster_avatar(
    size=300,
    body_color=None,
    eye_color=None,
    mouth_color=None,
    accent_colors=None,
    output_format='PIL'
):
    """
    Create a cute fuzzy monster avatar using Pillow.
    
    Args:
        size: Canvas size in pixels (default: 300)
        body_color: Hex color for body (random if None)
        eye_color: Hex color for eyes (default: black)
        mouth_color: Hex color for mouth (default: pink)
        accent_colors: List of colors for fuzzy details
        output_format: 'PIL' for Image object, 'base64' for base64 string, 'bytes' for PNG bytes
    
    Returns:
        PIL Image, base64 string, or bytes depending on output_format
    """
    
    # Cute color palette
    cute_palette = [
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
    
    # Set colors
    if body_color is None:
        body_color = random.choice(cute_palette)
    if eye_color is None:
        eye_color = '#000000'
    if mouth_color is None:
        mouth_color = random.choice(['#FF6B9D', '#FF6F61'])
    if accent_colors is None:
        accent_colors = random.sample(cute_palette, 2)
    
    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    body_rgb = hex_to_rgb(body_color)
    eye_rgb = hex_to_rgb(eye_color)
    mouth_rgb = hex_to_rgb(mouth_color)
    accent_rgb = [hex_to_rgb(c) for c in accent_colors]
    
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='#F0F8FF')
    draw = ImageDraw.Draw(img, 'RGBA')
    
    center_x = size // 2
    center_y = size // 2
    
    # Draw fuzzy body (round) with shadow
    body_radius = 70
    shadow_offset = 3
    
    # Shadow
    draw.ellipse(
        [center_x - body_radius + shadow_offset, center_y - body_radius + shadow_offset,
         center_x + body_radius + shadow_offset, center_y + body_radius + shadow_offset],
        fill=(0, 0, 0, 40)
    )
    
    # Main body
    draw.ellipse(
        [center_x - body_radius, center_y - body_radius,
         center_x + body_radius, center_y + body_radius],
        fill=body_rgb
    )
    
    # Add fuzzy texture with small circles
    random.seed(hash(body_color))  # Consistent fuzzy pattern for same color
    for _ in range(15):
        x = center_x + random.randint(-body_radius, body_radius)
        y = center_y + random.randint(-body_radius, body_radius)
        fuzz_size = random.randint(3, 8)
        fuzz_color = tuple(min(c + 30, 255) for c in body_rgb)  # Lighter shade
        draw.ellipse(
            [x - fuzz_size, y - fuzz_size, x + fuzz_size, y + fuzz_size],
            fill=fuzz_color
        )
    
    # Draw BIG cute eyes
    eye_radius = 18
    left_eye_x = center_x - 30
    right_eye_x = center_x + 30
    eye_y = center_y - 15
    
    # Left eye
    draw.ellipse(
        [left_eye_x - eye_radius, eye_y - eye_radius,
         left_eye_x + eye_radius, eye_y + eye_radius],
        fill=(255, 255, 255)  # White
    )
    # Left iris
    draw.ellipse(
        [left_eye_x - 10, eye_y - 8,
         left_eye_x + 6, eye_y + 8],
        fill=eye_rgb
    )
    # Left eye shine (for cuteness!)
    draw.ellipse(
        [left_eye_x - 6, eye_y - 4,
         left_eye_x - 2, eye_y],
        fill=(255, 255, 255)
    )
    
    # Right eye
    draw.ellipse(
        [right_eye_x - eye_radius, eye_y - eye_radius,
         right_eye_x + eye_radius, eye_y + eye_radius],
        fill=(255, 255, 255)
    )
    # Right iris
    draw.ellipse(
        [right_eye_x - 6, eye_y - 8,
         right_eye_x + 10, eye_y + 8],
        fill=eye_rgb
    )
    # Right eye shine
    draw.ellipse(
        [right_eye_x + 2, eye_y - 4,
         right_eye_x + 6, eye_y],
        fill=(255, 255, 255)
    )
    
    # Draw cute smile/mouth
    mouth_y = center_y + 25
    # Curved smile
    for i in range(-25, 26, 2):
        offset = abs(i) * 0.01  # Parabola effect
        draw.ellipse(
            [center_x + i - 1, mouth_y + int(offset) - 2,
             center_x + i + 1, mouth_y + int(offset) + 2],
            fill=mouth_rgb
        )
    
    # Add cute cheeks
    cheek_color = tuple(min(c + 60, 255) for c in mouth_rgb)
    draw.ellipse(
        [center_x - 60, center_y + 5, center_x - 40, center_y + 25],
        fill=cheek_color + (100,)  # Semi-transparent
    )
    draw.ellipse(
        [center_x + 40, center_y + 5, center_x + 60, center_y + 25],
        fill=cheek_color + (100,)
    )
    
    # Add fuzzy ears (optional)
    ear_color = body_rgb
    # Left ear
    draw.ellipse(
        [center_x - 85, center_y - 75, center_x - 55, center_y - 30],
        fill=ear_color
    )
    # Right ear
    draw.ellipse(
        [center_x + 55, center_y - 75, center_x + 85, center_y - 30],
        fill=ear_color
    )
    
    # Add inner ear
    inner_ear_color = tuple(min(c + 40, 255) for c in body_rgb)
    draw.ellipse(
        [center_x - 75, center_y - 65, center_x - 65, center_y - 40],
        fill=inner_ear_color
    )
    draw.ellipse(
        [center_x + 65, center_y - 65, center_x + 75, center_y - 40],
        fill=inner_ear_color
    )
    
    # Apply slight blur for fuzzy effect
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Return in requested format
    if output_format == 'base64':
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str
    elif output_format == 'bytes':
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
    else:  # 'PIL'
        return img


def create_multiple_monsters(count=5, size=300):
    """
    Generate multiple random cute monster avatars.
    
    Args:
        count: Number of avatars to generate
        size: Size of each avatar
    
    Returns:
        List of PIL Image objects
    """
    return [create_monster_avatar(size=size, output_format='PIL') for _ in range(count)]


def save_avatar_to_file(filename, size=300, body_color=None, eye_color=None, mouth_color=None):
    """
    Generate and save avatar to file.
    
    Args:
        filename: Path to save the PNG file
        size: Avatar size
        body_color: Body color (hex)
        eye_color: Eye color (hex)
        mouth_color: Mouth color (hex)
    
    Returns:
        Path to saved file
    """
    img = create_monster_avatar(
        size=size,
        body_color=body_color,
        eye_color=eye_color,
        mouth_color=mouth_color,
        output_format='PIL'
    )
    img.save(filename)
    return filename


# Quick test
if __name__ == '__main__':
    import os
    
    # Create a sample avatar
    print("🎨 Creating cute fuzzy monster avatar...")
    monster = create_monster_avatar(size=300, output_format='PIL')
    
    # Save it
    output_path = 'cute_monster.png'
    monster.save(output_path)
    print(f"✓ Saved to {output_path}")
    
    # Create a few random ones
    print("\n🎲 Creating 3 random monsters...")
    for i in range(3):
        avatar = create_monster_avatar(size=200, output_format='PIL')
        filename = f'monster_{i+1}.png'
        avatar.save(filename)
        print(f"✓ Saved {filename}")
    
    print("\n✨ Done! Check the generated PNG files.")
