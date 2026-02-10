# Three.js 3D Avatar System

A sophisticated 3D character avatar system using Three.js with stylized shaders, glTF-ready models, and interactive controls.

## Features

### 🎨 Visual Rendering
- **Real-time 3D rendering** with Three.js GPU acceleration
- **Stylized shaders** for cartoon/cell-shading appearance
- **Shadow mapping** for depth and realism
- **Post-processing effects** (FXAA antialiasing)
- **Dynamic lighting** with key, fill, rim, and ambient lights

### 🎭 Avatar Themes
Eight unique character themes with distinct accessories:

1. **Mario** - Classic plumber with cap
2. **Unicorn** - Magical creature with horn
3. **Dinosaur** - Prehistoric beast with spikes
4. **Dragon** - Fantasy creature with wings
5. **Knight** - Medieval warrior with armor
6. **Princess** - Royal character with crown
7. **Wizard** - Magical mage with hat
8. **Astronaut** - Space explorer with helmet

### 🖱️ Interaction
- **OrbitControls** - Drag to rotate, scroll to zoom
- **Auto-rotation** - Optional automatic spinning
- **Interactive mode** - Toggle user controls on/off
- **Responsive** - Adapts to container dimensions

### ⚙️ Customization
- Theme selection
- Size configuration
- Background color customization
- Auto-rotation control
- Interactive control toggle

## Installation

### Dependencies
```bash
npm install three@latest
npm install @react-three/fiber@latest
npm install @react-three/drei@latest
npm install @react-three/postprocessing@latest
```

## Usage

### Basic Component Usage

```jsx
import Avatar3D from './components/Avatar3D';

export default function App() {
  return (
    <Avatar3D 
      theme="mario"
      size={400}
      interactive={true}
      autoRotate={true}
      backgroundColor="#f0f0f0"
    />
  );
}
```

### With Theme Selector

```jsx
import AvatarShowcase from './components/AvatarShowcase';

export default function App() {
  return <AvatarShowcase />;
}
```

## Component Props

### Avatar3D

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `theme` | string | 'mario' | Character theme to display |
| `size` | number | 300 | Canvas size in pixels (square) |
| `interactive` | boolean | true | Enable mouse controls |
| `autoRotate` | boolean | true | Enable auto-rotation |
| `backgroundColor` | string | '#f0f0f0' | Canvas background color |

## Architecture

### Component Structure

```
Avatar3D.jsx
├── Scene Setup (Three.js)
├── Camera & Renderer
├── Post-processing (EffectComposer)
├── Lighting System
├── Character Model
│   ├── Body
│   ├── Head
│   └── Accessories
└── Controls (OrbitControls)
```

### Shader System

Located in `shaders/ToonShaders.js`:

- **ToonMaterial** - Cartoon/toon shading with color banding
- **CellShadeMaterial** - Cell-shaded comic book style
- **WatercolorMaterial** - Soft artistic appearance
- **OutlinePass** - Black outline rendering

### Theme Configuration

```javascript
const THEME_CONFIGS = {
  mario: {
    bodyColor: 0xE52B50,
    accentColor: 0x0D47A1,
    skinColor: 0xFFB347,
    eyeColor: 0x000000,
    mouthColor: 0xFF6B9D,
    accessories: [
      { type: 'hat', color: 0xE52B50 }
    ],
  },
  // ... more themes
}
```

## Creating Custom Themes

### Add a New Theme

1. Define theme configuration:
```javascript
const customTheme = {
  bodyColor: 0x12345A,
  accentColor: 0xABCDEF,
  skinColor: 0xFFB347,
  eyeColor: 0x000000,
  mouthColor: 0xFF6B9D,
  accessories: [
    { type: 'hat', color: 0xABCDEF },
    { type: 'wings', color: 0x12345A }
  ],
};
```

2. Add to `THEME_CONFIGS`:
```javascript
THEME_CONFIGS.customTheme = customTheme;
```

3. Use in component:
```jsx
<Avatar3D theme="customTheme" />
```

## Customizing Accessories

### Available Accessory Types

- **hat** - Simple cone hat with brim
- **horn** - Single horn on top of head
- **wings** - Wings on back
- **tail** - Tail extending from body
- **crown** - Royal crown with jewels

### Example Custom Accessory

```jsx
const customAccessory = {
  type: 'hat',
  color: 0xFF0000,
};
```

## Lighting Setup

The system uses a professional four-light setup:

1. **Key Light** - Main directional light (top-left)
2. **Fill Light** - Soft secondary light (opposite side)
3. **Rim Light** - Backlighting for silhouette (behind)
4. **Ambient Light** - Overall illumination

## Performance Optimization

### Rendering Performance

- **GPU Acceleration** - Uses WebGL for hardware rendering
- **Efficient Geometry** - Uses Three.js primitives (spheres, boxes)
- **Culling** - Automatic frustum culling
- **LOD** - Simple geometry reduces overdraw

### Tips for Better Performance

```jsx
// Disable interactive controls if not needed
<Avatar3D interactive={false} />

// Reduce size for lower-end devices
<Avatar3D size={200} />

// Disable auto-rotate if static display is needed
<Avatar3D autoRotate={false} />
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 15+
- Mobile browsers with WebGL support

## Advanced Customization

### Custom Shader Materials

```javascript
import { createToonMaterial } from './shaders/ToonShaders.js';

const customMaterial = createToonMaterial(0xFF0000, {
  bands: 5,
  outlineSize: 0.08,
  specularPower: 48,
});
```

### Post-Processing Effects

```javascript
// In Avatar3D component, customize EffectComposer
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
// Add custom passes here
```

## Troubleshooting

### Avatar not rendering
- Check browser WebGL support
- Verify all dependencies are installed
- Check console for errors

### Poor performance
- Reduce `size` prop
- Disable `interactive` mode if not needed
- Check GPU acceleration is enabled

### Shaders not working
- Ensure Three.js version matches
- Verify shader syntax
- Check shader uniform declarations

## Future Features

- [ ] Loading external glTF models
- [ ] Animation support (walk, idle, jump)
- [ ] More shader types (cell-shade, watercolor)
- [ ] Customizable body proportions
- [ ] Particle effects (magic, sparkles)
- [ ] Voice chat integrated avatars
- [ ] Avatar recording/export

## License

Part of inq-education project

## Contributing

To add new themes or accessories, follow the pattern established in `THEME_CONFIGS` and submit a PR.

---

**Created**: February 2026
**Framework**: React + Three.js
**Rendering**: WebGL with Post-processing
