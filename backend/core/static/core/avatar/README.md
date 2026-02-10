# Avatar Assets Directory

This directory contains layered PNG assets for anime-style avatar customization.

## Directory Structure

```
avatar/
├─ base/          # Base face shapes
├─ hair/          # Hair styles
├─ eyes/          # Eye styles
├─ mouth/         # Mouth expressions
├─ clothes/       # Clothing/outfits
└─ accessories/   # Accessories (glasses, hats, bows, etc.)
```

## How to Add Avatar Assets

### 1. Create PNG Layers (400x400px recommended)

Each PNG should be:
- **Transparent background** (RGBA format)
- **400x400 pixels** (or will be resized)
- **Centered** on canvas
- **Consistent style** across all layers

### 2. Naming Convention

Files should match the choice values in [`models.py`](../../models.py):

**Base Faces:**
- `round.png`
- `oval.png`

**Hair Styles:**
- `short_brown.png`
- `long_black.png`
- `medium_blonde.png`
- `spiky_red.png`

**Eyes:**
- `happy_blue.png`
- `sleepy_green.png`
- `cute_brown.png`
- `sparkle_purple.png`

**Mouth:**
- `smile.png`
- `open.png`
- `neutral.png`
- `small.png`

**Clothes:**
- `teacher_cardigan.png`
- `teacher_blazer.png`
- `student_uniform.png`
- `student_hoodie.png`
- `casual_shirt.png`

**Accessories:**
- `glasses.png`
- `badge.png`
- `bow.png`
- `hat.png`

### 3. Layer Order (Back → Front)

Assets are composed in this order:
1. Base face
2. Hair (back layer)
3. Eyes
4. Mouth
5. Clothes
6. Accessories (accessory_1)
7. Accessories (accessory_2)

### 4. Color Tinting

Some layers support color tinting:
- **Base face**: Applies `skinTone` color
- **Hair**: Applies `hairColor` color

### 5. Creating Assets with AI

Recommended tools:
- **Leonardo AI** (anime art models)
- **Stable Diffusion** with anime checkpoints
- **Midjourney** (--niji mode)

**Example prompt:**
```
anime style cute [feature] for avatar, transparent background, 
centered, simple clean design, pastel colors, friendly look, 
no background, PNG format
```

### 6. Expanding Options

To add new variations:

1. **Add PNG file** to appropriate directory
2. **Update [`models.py`](../../models.py)** - add choice to relevant tuple:
   ```python
   HAIR_CHOICES = (
       ('short_brown', 'Short Brown'),
       ('your_new_style', 'Your New Style Name'),  # Add here
   )
   ```
3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Update UI** (optional) - add option to avatar builder dropdown

### 7. Placeholder System

If no PNG exists, the renderer creates a simple placeholder circle with:
- Skin tone color
- Basic face features (eyes, mouth)
- Outline

## Tips for Artists

- **Keep it simple**: Avoid overly detailed illustrations
- **Consistent proportions**: Ensure eyes/mouths align across variations
- **Leave space**: Don't extend to canvas edges (padding ~20px)
- **Test combinations**: Preview how layers look together
- **Export at 2x**: 800x800px then downscale for crisp edges

## Teacher vs Student Differentiation

Subtle differences through clothing:
- **Teachers**: Cardigans, blazers, glasses, neutral colors
- **Students**: Uniforms, hoodies, bright colors, playful accessories

## Example Workflow

1. Design base face in Illustrator/Procreate
2. Export face as `round.png` (transparent BG)
3. Place in `avatar/base/` directory
4. Test by accessing profile page and selecting "round" face
5. Repeat for other layers

## Current Status

⚠️ **Assets Not Yet Created**

The system will render placeholders until you add PNG files.

To get started:
- Add at least 1-2 files per category
- Test avatar builder to see results
- Expand library over time

## Questions?

See main [`avatar_renderer.py`](../../../../avatar_renderer.py) for rendering logic
See [`models.py`](../../models.py) for available choices
