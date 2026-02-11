# 🧟 PixiJS Monster Avatar System

## Overview

A ClassDojo-style monster avatar system built with **PixiJS** for rendering and **Django** for persistence. Features real-time animations, customizable traits, and modular sprite architecture.

---

## ✨ Features

- **Sprite-Based Architecture**: Modular body parts (body, eyes, mouth, arms, accessories)
- **Live Animations**: Breathing, blinking, arm movements for engaging UX
- **Real-Time Customization**: Instant preview as users change traits
- **Persistent Storage**: Avatar traits saved per user via Django ORM
- **RESTful API**: Clean endpoints for GET, POST, and randomize operations
- **Responsive Design**: Works on all screen sizes

---

## 🏗️ Architecture

### Backend (Django)

#### Models ([models.py](backend/core/models.py))

```python
class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    
    # Trait selections
    body_type = models.CharField(max_length=20, choices=BODY_TYPES, default='round_blue')
    eye_type = models.CharField(max_length=20, choices=EYE_TYPES, default='big_happy')
    mouth_type = models.CharField(max_length=20, choices=MOUTH_TYPES, default='smile')
    accessory = models.CharField(max_length=20, choices=ACCESSORY_TYPES, default='none')
    
    # Custom colors
    primary_color = models.CharField(max_length=7, default='#FF6B9D')
    accent_color = models.CharField(max_length=7, default='#FFB347')
```

#### API Endpoints ([urls.py](backend/core/urls.py))

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/avatar/` | Get user's avatar data |
| POST | `/api/avatar/save/` | Save avatar traits |
| GET | `/api/avatar/randomize/` | Generate random avatar |

### Frontend (React + PixiJS)

#### Components

1. **MonsterAvatar.js** - PixiJS rendering component with animations
2. **AvatarCustomizer.js** - Full customization UI with real-time preview

#### Trait Options

| Part | Options |
|------|---------|
| **Body** | round_blue, round_pink, round_green, round_yellow, square_purple, square_orange |
| **Eyes** | big_happy, big_sleepy, small_angry, round_confused, star_sparkly |
| **Mouth** | smile, grin, open, neutral, tongue |
| **Accessory** | none, cap, hat, crown, glasses, bow |

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Create migration
cd backend
python manage.py migrate

# Run server
python manage.py runserver
```

### 2. Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start React dev server
npm start
```

### 3. Access

- **Django Profile Pages**: `http://localhost:8000/profile/`
- **React Avatar Customizer**: `http://localhost:3000/`

---

## 🎨 Usage

### Display Avatar on Profile Page

The avatar automatically renders on student and teacher profile pages using the Django template:

```django
{% include "core/avatar_display.html" %}
```

### Customize Avatar

1. Navigate to profile page
2. Click **"🎨 Customize Avatar"** button
3. Opens React customizer in new tab
4. Select traits and colors
5. Click **"💾 Save Avatar"**

### Programmatic Avatar Creation

```python
from core.models import Avatar

# Create avatar for user
avatar = Avatar.objects.create(
    user=user,
    body_type='round_blue',
    eye_type='big_happy',
    mouth_type='smile',
    accessory='cap',
    primary_color='#FF6B9D',
    accent_color='#FFB347'
)
```

---

## 🎭 Animation System

The PixiJS renderer includes three animated behaviors:

### 1. **Breathing/Bouncing**
```javascript
monster.scale.y = 1 + Math.sin(time * 2) * 0.03;
monster.rotation = Math.sin(time * 1.5) * 0.02;
```

### 2. **Eye Blinking**
```javascript
const blinkCycle = (Math.sin(time * 0.5) + 1) / 2;
eyesContainer.scale.y = blinkCycle > 0.9 || blinkCycle < 0.1 ? 0.1 : 1;
```

### 3. **Arm Waving**
```javascript
leftArm.rotation = Math.sin(time * 1.5) * 0.4 - 0.2;
rightArm.rotation = Math.sin(time * 1.5 + Math.PI) * 0.4 + 0.2;
```

---

## 📁 File Structure

```
myproject/
├── backend/
│   └── core/
│       ├── models.py                 # Avatar model
│       ├── views.py                  # API endpoints
│       ├── urls.py                   # URL routing
│       ├── serializers.py            # Avatar serializer
│       ├── migrations/
│       │   └── 0028_avatar.py        # Avatar migration
│       └── templates/
│           └── core/
│               ├── avatar_display.html        # Django template
│               ├── student_profile.html
│               └── teacher_profile.html
└── frontend/
    └── src/
        ├── components/
        │   ├── MonsterAvatar.js      # PixiJS renderer
        │   └── AvatarCustomizer.js   # Customization UI
        └── css/
            ├── MonsterAvatar.css
            └── AvatarCustomizer.css
```

---

## 🔧 Customization

### Add New Body Parts

To add a new body type:

1. Update Avatar model choices:
```python
BODY_TYPES = (
    ('round_blue', 'Round Blue'),
    ('new_type', 'New Type'),  # Add here
)
```

2. Create migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Update frontend renderer:
```javascript
const createBodyGraphic = (bodyType, color) => {
    // Handle new type
    if (bodyType === 'new_type') {
        // ... draw new shape
    }
};
```

### Change Animation Speed

Adjust timing parameters in MonsterAvatar.js:

```javascript
time += 0.01;  // Increase for faster animation
monster.scale.y = 1 + Math.sin(time * 2) * 0.03;  // Adjust multiplier
```

---

## 🐛 Troubleshooting

### Avatar Not Displaying
- Check browser console for PixiJS errors
- Verify avatar data exists: `/api/avatar/`
- Ensure PixiJS CDN is loaded (check network tab)

### Save Button Not Working
- Verify CSRF token is present in template
- Check Django logs for API errors
- Confirm user is authenticated

### Animation Laggy
- Reduce animation complexity
- Lower canvas resolution
- Use fewer sprite layers

---

## 🎯 Why This Architecture?

| Requirement | Solution |
|-------------|----------|
| **Fast Loading** | PNG sprites (or procedural graphics) |
| **Low-End Devices** | Canvas/WebGL optimization |
| **Millions of Combos** | Modular trait system |
| **Cute Not Creepy** | Stylized 2D design |
| **Easy Rewards** | Simple trait swapping |
| **Persistent** | Django ORM storage |

---

## 📚 Tech Stack

- **PixiJS 7.2.4** - 2D WebGL rendering
- **React 18** - UI framework
- **Django 4.x** - Backend framework
- **Django REST Framework** - API layer

---

## 🚀 Future Enhancements

- [ ] PNG sprite assets for each trait variant
- [ ] More accessory options (hats, glasses, etc.)
- [ ] Animation presets (happy, sad, excited)
- [ ] Avatar sharing/export as PNG
- [ ] Reward system (unlock accessories)
- [ ] Mobile app integration

---

## 📝 License

Part of the InqEd educational platform.

---

## 🤝 Contributing

1. Add new traits to `models.py`
2. Create corresponding graphics in `MonsterAvatar.js`
3. Update customizer UI options
4. Test on multiple browsers
5. Submit pull request

---

**Built with ❤️ for education platforms**
