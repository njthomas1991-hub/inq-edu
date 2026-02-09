# 🎨 Monster Avatar Generator

A Python utility for generating cute, fuzzy monster avatars with random colors, big eyes, and smiling faces.

## Features

- **Cute-biased generation**: Optimized for adorable monster designs
- **Random color palettes**: Bright, cheerful colors
- **Customizable attributes**: Body shape, limbs, eyes, mouth, accessories
- **Django integration**: Save directly to user profiles
- **API endpoints**: RESTful endpoints for frontend integration

## Installation

The avatar generator is already integrated into your Django app at:
```
backend/core/avatar_generator.py
```

## Usage

### 1. Generate Avatar Data (No Database)

```python
from core.avatar_generator import create_monster_avatar

# Generate a cute monster (not saved to database)
avatar = create_monster_avatar(user=None, cute_bias=True)

# Access attributes
print(f"Body: {avatar.body_shape} in {avatar.body_color}")
print(f"Eyes: {avatar.eye_style} ({avatar.eye_color})")
print(f"Mouth: {avatar.mouth_style} ({avatar.mouth_color})")
```

### 2. Create and Save Avatar for User

```python
from core.avatar_generator import create_monster_avatar
from core.models import User

# Get a user
user = User.objects.get(username='admin')

# Generate and save cute monster avatar
avatar = create_monster_avatar(user=user, cute_bias=True)
# Avatar is automatically saved to database
```

### 3. Get Random Avatar Data (for JSON responses)

```python
from core.avatar_generator import get_random_avatar_data

# Get dictionary of avatar attributes
avatar_data = get_random_avatar_data()
# Returns: {'body_shape': 'round', 'body_color': '#FF6B9D', ...}
```

### 4. Use in Django Views

```python
from django.http import JsonResponse
from core.avatar_generator import create_monster_avatar

def my_view(request):
    # Generate avatar for current user
    avatar = create_monster_avatar(user=request.user, cute_bias=True)
    
    return JsonResponse({
        'success': True,
        'avatar': avatar.to_dict()
    })
```

## API Endpoints

### GET `/avatar/generate/`
Returns random avatar data (no save).

**Response:**
```json
{
  "success": true,
  "avatar": {
    "body_shape": "round",
    "body_color": "#FF6B9D",
    "arm_style": "short",
    "eye_style": "round",
    "mouth_style": "smile",
    ...
  }
}
```

### POST `/avatar/auto-generate/`
Auto-generates and saves a cute monster avatar for the authenticated user.

**Response:**
```json
{
  "success": true,
  "message": "Avatar auto-generated successfully",
  "avatar": { ... }
}
```

### POST `/avatar/save/`
Saves a custom avatar configuration.

**Request Body:**
```json
{
  "bodyShape": "round",
  "bodyColor": "#FF6B9D",
  "armStyle": "short",
  ...
}
```

## Avatar Attributes

### Body
- **Shapes**: `round`, `oval`, `square`, `rectangular`
- **Color**: Hex color code

### Limbs
- **Arm styles**: `short`, `long`, `tentacle`, `none`
- **Leg styles**: `two`, `four`, `none`
- **Colors**: Hex color codes

### Face
- **Eye styles**: `round` (big eyes), `oval`, `closed`, `star`
- **Mouth styles**: `smile`, `frown`, `neutral`, `open`
- **Has teeth**: Boolean

### Accessories
- **Glasses**: Boolean
- **Ears**: Boolean (fuzzy!)
- **Antennae**: Boolean
- **Shoes**: Boolean with color

## Customization

### Change Cute Bias

```python
# Fully random monster (any shape, style, color)
avatar = create_monster_avatar(user=user, cute_bias=False)
```

### Add Custom Color Palette

Edit `avatar_generator.py`:

```python
cute_colors = [
    '#FF6B9D',  # Pink
    '#YOUR_COLOR',  # Add your color
    ...
]
```

## Examples

### Example 1: Batch Generate for All Users

```python
from core.models import User
from core.avatar_generator import create_monster_avatar

# Give all users without avatars a random cute monster
users_without_avatars = User.objects.filter(avatar__isnull=True)

for user in users_without_avatars:
    create_monster_avatar(user=user, cute_bias=True)
    print(f"✅ Generated avatar for {user.username}")
```

### Example 2: Management Command

Create `backend/core/management/commands/generate_avatars.py`:

```python
from django.core.management.base import BaseCommand
from core.models import User
from core.avatar_generator import create_monster_avatar

class Command(BaseCommand):
    help = 'Generate cute monster avatars for all users'

    def handle(self, *args, **options):
        users = User.objects.filter(avatar__isnull=True)
        
        for user in users:
            create_monster_avatar(user=user, cute_bias=True)
            self.stdout.write(
                self.style.SUCCESS(f'Generated avatar for {user.username}')
            )
```

Run with: `python manage.py generate_avatars`

### Example 3: Registration Hook

Add to signup view to auto-generate avatars:

```python
from core.avatar_generator import create_monster_avatar

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-generate cute avatar for new user
            create_monster_avatar(user=user, cute_bias=True)
            
            login(request, user)
            return redirect('dashboard')
```

## Testing

Run the test script:

```bash
python test_avatar_generator.py
```

Expected output:
```
🎨 Testing Monster Avatar Generator
✨ Generating cute fuzzy monster avatar...
🦄 Your Cute Monster:
  Body:       OVAL shape
  Color:      #FF6B9D
  Eyes:       ROUND 👀
  Mouth:      SMILE 😊
  ...
```

## Integration with Frontend

The JavaScript avatar builder already has a randomize function. To use the Python generator on the frontend:

1. Call the `/avatar/auto-generate/` endpoint
2. Receive avatar data
3. Update the avatar builder form
4. Render the avatar

```javascript
// In avatar_builder.html
async function pythonRandomize() {
    const response = await fetch('/avatar/auto-generate/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    });
    
    const data = await response.json();
    if (data.success) {
        // Avatar already saved, just reload page
        window.location.reload();
    }
}
```

## Color Palette

**Cute Colors (Default):**
- Pink: `#FF6B9D`, `#C44569`
- Blue: `#4A90E2`, `#00D2FF`
- Green: `#50C878`
- Orange: `#FFB347`, `#FFA500`
- Purple: `#B39DDB`, `#6C5CE7`
- Coral: `#FF6F61`

## Function Reference

### `create_monster_avatar(user=None, cute_bias=True)`

Generate a monster avatar.

**Parameters:**
- `user` (User, optional): Django User instance to attach avatar to
- `cute_bias` (bool): If True, biases towards cute features (default: True)

**Returns:**
- Avatar instance (saved if user provided, unsaved otherwise)

### `get_random_avatar_data()`

Generate random avatar data as a dictionary.

**Returns:**
- Dictionary with avatar configuration

### `generate_avatar_for_user(user)`

Convenience function to generate and save a cute monster avatar.

**Parameters:**
- `user` (User): Django User instance

**Returns:**
- Avatar instance (saved)

## License

Part of the INQ-ED project.
