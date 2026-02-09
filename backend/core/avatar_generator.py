import random
from .models import Avatar


def create_monster_avatar(user=None, cute_bias=True):
    """
    Generate a cute fuzzy monster avatar with random colors, big eyes, and a smile.
    
    Args:
        user: User instance to attach the avatar to (optional)
        cute_bias: If True, biases towards cute features (default: True)
    
    Returns:
        Avatar instance (unsaved if no user provided)
    """
    # Cute color palette - bright and cheerful
    cute_colors = [
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
    
    # All possible colors for variety
    all_colors = cute_colors + [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00',
        '#FF00FF', '#00FFFF', '#800080', '#FFA500'
    ]
    
    if cute_bias:
        # Cute monster configuration
        body_shape = random.choice(['round', 'oval'])
        body_color = random.choice(cute_colors)
        arm_style = random.choice(['short', 'long'])
        arm_color = random.choice(cute_colors)
        leg_style = 'two'
        leg_color = random.choice(cute_colors)
        eye_style = 'round'  # Big round eyes for cuteness
        eye_color = random.choice(['#000000', '#4A90E2', '#50C878'])
        mouth_style = 'smile'  # Always smiling
        mouth_color = random.choice(['#FF6B9D', '#FF6F61', '#000000'])
        has_teeth = False  # No teeth for maximum cuteness
        has_glasses = random.choice([True, False])
        has_ears = True  # Fuzzy ears
        has_antennae = random.choice([True, False])
        has_shoes = random.choice([True, False])
        shoe_color = random.choice(cute_colors) if has_shoes else None
    else:
        # Fully random configuration
        body_shape = random.choice(['round', 'square', 'rectangular', 'oval'])
        body_color = random.choice(all_colors)
        arm_style = random.choice(['short', 'long', 'tentacle', 'none'])
        arm_color = random.choice(all_colors)
        leg_style = random.choice(['two', 'four', 'none'])
        leg_color = random.choice(all_colors)
        eye_style = random.choice(['round', 'oval', 'closed', 'star'])
        eye_color = random.choice(all_colors)
        mouth_style = random.choice(['smile', 'frown', 'neutral', 'open'])
        mouth_color = random.choice(all_colors)
        has_teeth = random.choice([True, False])
        has_glasses = random.choice([True, False])
        has_ears = random.choice([True, False])
        has_antennae = random.choice([True, False])
        has_shoes = random.choice([True, False])
        shoe_color = random.choice(all_colors) if has_shoes else None
    
    # Create avatar instance
    avatar_data = {
        'body_shape': body_shape,
        'body_color': body_color,
        'arm_style': arm_style,
        'arm_color': arm_color,
        'leg_style': leg_style,
        'leg_color': leg_color,
        'eye_style': eye_style,
        'eye_color': eye_color,
        'mouth_style': mouth_style,
        'mouth_color': mouth_color,
        'has_teeth': has_teeth,
        'has_glasses': has_glasses,
        'has_ears': has_ears,
        'has_antennae': has_antennae,
        'has_shoes': has_shoes,
        'shoe_color': shoe_color,
    }
    
    if user:
        # Create or update avatar for the user
        avatar, created = Avatar.objects.update_or_create(
            user=user,
            defaults=avatar_data
        )
        return avatar
    else:
        # Return unsaved avatar instance
        return Avatar(**avatar_data)


def generate_avatar_for_user(user):
    """
    Convenience function to generate and save a cute monster avatar for a user.
    
    Args:
        user: User instance
    
    Returns:
        Avatar instance (saved)
    """
    return create_monster_avatar(user=user, cute_bias=True)


def get_random_avatar_data():
    """
    Generate random avatar data as a dictionary (for JSON responses).
    
    Returns:
        Dictionary with avatar configuration
    """
    avatar = create_monster_avatar(user=None, cute_bias=True)
    return avatar.to_dict() if hasattr(avatar, 'to_dict') else {
        'body_shape': avatar.body_shape,
        'body_color': avatar.body_color,
        'arm_style': avatar.arm_style,
        'arm_color': avatar.arm_color,
        'leg_style': avatar.leg_style,
        'leg_color': avatar.leg_color,
        'eye_style': avatar.eye_style,
        'eye_color': avatar.eye_color,
        'mouth_style': avatar.mouth_style,
        'mouth_color': avatar.mouth_color,
        'has_teeth': avatar.has_teeth,
        'has_glasses': avatar.has_glasses,
        'has_ears': avatar.has_ears,
        'has_antennae': avatar.has_antennae,
        'has_shoes': avatar.has_shoes,
        'shoe_color': avatar.shoe_color,
    }
