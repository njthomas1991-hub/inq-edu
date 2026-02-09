"""
Avatar Image Renderer - Generates PNG images from avatar data using Pillow.

This module converts Avatar model data into beautiful PNG images with:
- Pillow (PIL) rendering engine for high-quality graphics
- Drawing of body shapes, limbs, face features, and accessories
- Color parsing from hex strings
- Base64 encoding for web embedding
- Support for multiple output formats

Key Functions:
- generate_avatar_image(): Create PIL Image from avatar data
- avatar_to_base64(): Convert to base64 PNG for <img> tags
- save_avatar_image(): Save to file or ContentFile for storage

Used by:
- profile_view: Generates avatar_image context for profile display
- save_avatar API: Returns rendered image after saving customizations
- auto_generate_avatar API: Returns generated image
- get_avatar_image API: Fetches rendered image for existing avatar

Example:
    from core.models import Avatar
    avatar = Avatar.objects.get(user=request.user)
    b64_img = avatar_to_base64(avatar.to_dict())
    # Use in template: <img src="data:image/png;base64,{{ b64_img }}" />
"""

from PIL import Image, ImageDraw
import io
import base64
from django.core.files.base import ContentFile


def generate_avatar_image(avatar_data, size=300):
    """
    Generate a PNG image of an avatar based on avatar data.
    
    Args:
        avatar_data: Dictionary with avatar configuration (from Avatar.to_dict())
        size: Canvas size in pixels (generates square image)
    
    Returns:
        PIL Image object
    """
    
    # Create a new image with light background
    img = Image.new('RGB', (size, size), color='#F8F9FA')
    draw = ImageDraw.Draw(img)
    
    # Parse colors
    body_color = avatar_data.get('bodyColor', '#FF6B9D')
    arm_color = avatar_data.get('armColor', '#FF6F61')
    leg_color = avatar_data.get('legColor', '#FF6B9D')
    eye_color = avatar_data.get('eyeColor', '#000000')
    mouth_color = avatar_data.get('mouthColor', '#FF6F61')
    shoe_color = avatar_data.get('shoeColor', '#000000')
    
    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    body_rgb = hex_to_rgb(body_color)
    arm_rgb = hex_to_rgb(arm_color)
    leg_rgb = hex_to_rgb(leg_color)
    eye_rgb = hex_to_rgb(eye_color)
    mouth_rgb = hex_to_rgb(mouth_color)
    shoe_rgb = hex_to_rgb(shoe_color)
    
    center_x, center_y = size // 2, size // 2
    
    # Draw body
    body_shape = avatar_data.get('bodyShape', 'round')
    if body_shape == 'round':
        draw.ellipse([center_x - 60, center_y - 70, center_x + 60, center_y + 80], fill=body_rgb)
    elif body_shape == 'oval':
        draw.ellipse([center_x - 55, center_y - 75, center_x + 55, center_y + 85], fill=body_rgb)
    elif body_shape == 'square':
        draw.rectangle([center_x - 60, center_y - 70, center_x + 60, center_y + 80], fill=body_rgb)
    elif body_shape == 'rectangular':
        draw.rectangle([center_x - 50, center_y - 80, center_x + 50, center_y + 85], fill=body_rgb)
    
    # Draw arms
    arm_style = avatar_data.get('armStyle', 'short')
    if arm_style == 'short':
        draw.line([(center_x - 60, center_y - 20), (center_x - 90, center_y - 10)], fill=arm_rgb, width=8)
        draw.line([(center_x + 60, center_y - 20), (center_x + 90, center_y - 10)], fill=arm_rgb, width=8)
    elif arm_style == 'long':
        draw.line([(center_x - 60, center_y), (center_x - 110, center_y + 20)], fill=arm_rgb, width=8)
        draw.line([(center_x + 60, center_y), (center_x + 110, center_y + 20)], fill=arm_rgb, width=8)
    elif arm_style == 'tentacle':
        draw.arc([(center_x - 100, center_y - 30), (center_x - 60, center_y)], 0, 180, fill=arm_rgb, width=8)
        draw.arc([(center_x + 60, center_y - 30), (center_x + 100, center_y)], 0, 180, fill=arm_rgb, width=8)
    
    # Draw legs
    leg_style = avatar_data.get('legStyle', 'two')
    if leg_style == 'two':
        draw.line([(center_x - 30, center_y + 75), (center_x - 30, center_y + 130)], fill=leg_rgb, width=12)
        draw.line([(center_x + 30, center_y + 75), (center_x + 30, center_y + 130)], fill=leg_rgb, width=12)
    elif leg_style == 'four':
        draw.line([(center_x - 40, center_y + 65), (center_x - 40, center_y + 130)], fill=leg_rgb, width=10)
        draw.line([(center_x - 10, center_y + 75), (center_x - 10, center_y + 130)], fill=leg_rgb, width=10)
        draw.line([(center_x + 10, center_y + 75), (center_x + 10, center_y + 130)], fill=leg_rgb, width=10)
        draw.line([(center_x + 40, center_y + 65), (center_x + 40, center_y + 130)], fill=leg_rgb, width=10)
    
    # Draw eyes
    eye_style = avatar_data.get('eyeStyle', 'round')
    eye_y = center_y - 10
    
    if eye_style == 'round':
        draw.ellipse([center_x - 42, eye_y - 12, center_x - 18, eye_y + 12], fill=eye_rgb)
        draw.ellipse([center_x + 18, eye_y - 12, center_x + 42, eye_y + 12], fill=eye_rgb)
    elif eye_style == 'oval':
        draw.ellipse([center_x - 42, eye_y - 18, center_x - 18, eye_y + 18], fill=eye_rgb)
        draw.ellipse([center_x + 18, eye_y - 18, center_x + 42, eye_y + 18], fill=eye_rgb)
    elif eye_style == 'closed':
        draw.line([(center_x - 42, eye_y), (center_x - 18, eye_y)], fill=eye_rgb, width=2)
        draw.line([(center_x + 18, eye_y), (center_x + 42, eye_y)], fill=eye_rgb, width=2)
    elif eye_style == 'star':
        # Draw star eyes - simplified
        draw.polygon([(center_x - 30, eye_y - 8), (center_x - 22, eye_y), (center_x - 26, eye_y + 8),
                     (center_x - 18, eye_y + 4), (center_x - 22, eye_y + 12), (center_x - 30, eye_y + 6)], fill=eye_rgb)
        draw.polygon([(center_x + 22, eye_y - 8), (center_x + 30, eye_y), (center_x + 26, eye_y + 8),
                     (center_x + 34, eye_y + 4), (center_x + 30, eye_y + 12), (center_x + 22, eye_y + 6)], fill=eye_rgb)
    
    # Draw mouth
    mouth_style = avatar_data.get('mouthStyle', 'smile')
    mouth_y = center_y + 25
    
    if mouth_style == 'smile':
        draw.arc([(center_x - 20, mouth_y), (center_x + 20, mouth_y + 15)], 0, 180, fill=mouth_rgb, width=3)
    elif mouth_style == 'frown':
        draw.arc([(center_x - 20, mouth_y - 15), (center_x + 20, mouth_y)], 180, 360, fill=mouth_rgb, width=3)
    elif mouth_style == 'neutral':
        draw.line([(center_x - 20, mouth_y), (center_x + 20, mouth_y)], fill=mouth_rgb, width=3)
    elif mouth_style == 'open':
        draw.ellipse([center_x - 15, mouth_y - 10, center_x + 15, mouth_y + 12], fill=mouth_rgb)
        # Draw teeth if applicable
        if avatar_data.get('hasTeeth', False):
            for i in range(-12, 13, 6):
                draw.rectangle([center_x + i, mouth_y - 3, center_x + i + 4, mouth_y + 5], fill=(255, 255, 255))
    
    # Draw accessories
    
    # Ears
    if avatar_data.get('hasEars', False):
        draw.ellipse([center_x - 85, center_y - 50, center_x - 45, center_y - 10], fill=body_rgb)
        draw.ellipse([center_x + 45, center_y - 50, center_x + 85, center_y - 10], fill=body_rgb)
    
    # Glasses
    if avatar_data.get('hasGlasses', False):
        draw.ellipse([center_x - 40, eye_y - 14, center_x - 20, eye_y + 14], outline=(51, 51, 51), width=2)
        draw.ellipse([center_x + 20, eye_y - 14, center_x + 40, eye_y + 14], outline=(51, 51, 51), width=2)
        draw.line([(center_x - 20, eye_y), (center_x + 20, eye_y)], fill=(51, 51, 51), width=2)
    
    # Antennae
    if avatar_data.get('hasAntennae', False):
        draw.line([(center_x - 40, center_y - 75), (center_x - 50, center_y - 120)], fill=(102, 102, 102), width=4)
        draw.line([(center_x + 40, center_y - 75), (center_x + 50, center_y - 120)], fill=(102, 102, 102), width=4)
        draw.ellipse([center_x - 58, center_y - 128, center_x - 42, center_y - 112], fill=(102, 102, 102))
        draw.ellipse([center_x + 42, center_y - 128, center_x + 58, center_y - 112], fill=(102, 102, 102))
    
    # Shoes
    if avatar_data.get('hasShoes', False):
        draw.rectangle([center_x - 35, center_y + 130, center_x - 17, center_y + 142], fill=shoe_rgb)
        draw.rectangle([center_x + 17, center_y + 130, center_x + 35, center_y + 142], fill=shoe_rgb)
    
    return img


def avatar_to_base64(avatar_data, size=300):
    """
    Convert avatar data to base64 PNG for embedding in HTML.
    
    Args:
        avatar_data: Dictionary with avatar configuration
        size: Canvas size
    
    Returns:
        Base64 string of PNG image
    """
    img = generate_avatar_image(avatar_data, size)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str


def save_avatar_image(avatar_instance, size=300):
    """
    Generate and save avatar image file to avatar instance.
    (For future Cloudinary integration)
    
    Args:
        avatar_instance: Avatar model instance
        size: Canvas size
    
    Returns:
        ContentFile object
    """
    img = generate_avatar_image(avatar_instance.to_dict(), size)
    
    # Save to BytesIO
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Return as ContentFile for model
    return ContentFile(buffer.getvalue(), name=f'avatar_{avatar_instance.user.id}.png')
