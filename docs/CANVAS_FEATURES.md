# 🎨 Canvas Features Documentation

## Overview

The avatar panel now includes comprehensive **HTML5 Canvas** features for exporting, manipulating, and downloading avatars in various formats and configurations.

---

## 📋 Table of Contents

1. [Export Formats](#export-formats)
2. [Canvas Methods](#canvas-methods)
3. [UI Controls](#ui-controls)
4. [Utility Functions](#utility-functions)
5. [Usage Examples](#usage-examples)
6. [Browser Compatibility](#browser-compatibility)

---

## 🖼️ Export Formats

### PNG Export
```javascript
const dataUrl = sceneRef.current.exportAsBase64();
// Returns: "data:image/png;base64,iVBORw0KGgo..."
```

**Features:**
- ✅ Lossless quality
- ✅ Transparent background support
- ✅ Best for web display
- 📦 Larger file size

### JPEG Export
```javascript
const dataUrl = sceneRef.current.exportAsJPEG(0.95);
// Quality: 0.0 to 1.0
```

**Features:**
- ✅ Smaller file size (60-80% smaller)
- ✅ Fast compression
- ❌ No transparency
- 📦 Lossy compression

### Blob Export
```javascript
const blob = await sceneRef.current.exportAsBlob('png', 1);
// Use for uploads or advanced processing
```

**Use Cases:**
- File uploads to server
- IndexedDB storage
- Service Worker caching
- Sharing via Web Share API

---

## 🛠️ Canvas Methods

### AvatarScene Methods

#### `exportAsBase64(quality)`
Export canvas as base64-encoded PNG.
```javascript
const img = sceneRef.current.exportAsBase64(1);
// quality: 0-1 (default: 1)
```

#### `exportAsJPEG(quality)`
Export canvas as base64-encoded JPEG.
```javascript
const img = sceneRef.current.exportAsJPEG(0.9);
// quality: 0-1 (default: 0.9)
```

#### `exportAsBlob(format, quality)`
Export as Blob for advanced use cases.
```javascript
const blob = await sceneRef.current.exportAsBlob('png', 1);
```

#### `captureRegion(rect)`
Capture a specific area of the canvas.
```javascript
const croppedImg = sceneRef.current.captureRegion({
    x: 50, y: 50, width: 300, height: 400
});
```

#### `createThumbnail(maxWidth, maxHeight)`
Generate a thumbnail version.
```javascript
const thumb = sceneRef.current.createThumbnail(200, 200);
```

#### `exportWithBackground(color)`
Add a solid background color.
```javascript
const withBg = sceneRef.current.exportWithBackground('#FFFFFF');
```

#### `exportAtResolution(width, height)`
Export at custom resolution.
```javascript
const hdImg = sceneRef.current.exportAtResolution(1920, 1080);
```

#### `copyToClipboard()`
Copy canvas image to system clipboard.
```javascript
const success = await sceneRef.current.copyToClipboard();
if (success) alert('Copied!');
```

#### `takeSnapshot()`
Capture avatar with metadata.
```javascript
const snapshot = sceneRef.current.takeSnapshot();
// Returns: { image, timestamp, avatarData, dimensions }
```

#### `getCanvasPixelData()`
Get raw pixel data for analysis.
```javascript
const imageData = sceneRef.current.getCanvasPixelData();
// Returns: ImageData object
```

#### `getCanvasContext()`
Get 2D rendering context for custom operations.
```javascript
const ctx = sceneRef.current.getCanvasContext();
ctx.filter = 'blur(5px)';
```

---

## 🎮 UI Controls

### Export Tab

Access via the **💾 Export** tab in the avatar panel.

#### Download Options

| Button | Format | Size | Use Case |
|--------|--------|------|----------|
| 🖼️ Download PNG | PNG | ~50-100KB | High quality, web |
| 📷 Download JPEG | JPEG | ~20-40KB | Smaller files |
| 🔍 Download Thumbnail | PNG 200x200 | ~10-20KB | Previews, icons |
| 🎬 Download HD | PNG 800x1000 | ~150-250KB | Print, high-res |

#### Background Options

Click colored squares to export with background:
- ⬜ White
- 🔳 Light Gray
- 🟪 Purple
- 🔵 Blue
- 🟢 Green
- ⬛ Black

#### Tools

- **📋 Copy to Clipboard**: Copy image for pasting into other apps
- **📸 Save Snapshot**: Save with metadata to localStorage

---

## 🧰 Utility Functions

Located in `/frontend/src/utils/canvasUtils.js`

### Import
```javascript
import * as CanvasUtils from './utils/canvasUtils';
// or
import { downloadCanvas, resizeCanvas } from './utils/canvasUtils';
```

### Available Utilities

#### `downloadCanvas(canvas, filename, format, quality)`
```javascript
CanvasUtils.downloadCanvas(canvas, 'my-avatar.png', 'png', 1);
```

#### `resizeCanvas(sourceCanvas, maxWidth, maxHeight)`
```javascript
const resized = CanvasUtils.resizeCanvas(canvas, 400, 500);
```

#### `addBackgroundToCanvas(sourceCanvas, color)`
```javascript
const withBg = CanvasUtils.addBackgroundToCanvas(canvas, '#FFFFFF');
```

#### `cropCanvas(sourceCanvas, rect)`
```javascript
const cropped = CanvasUtils.cropCanvas(canvas, {
    x: 50, y: 50, width: 200, height: 200
});
```

#### `applyFilterToCanvas(sourceCanvas, filter)`
```javascript
const filtered = CanvasUtils.applyFilterToCanvas(canvas, 'grayscale(100%)');
```

#### `mergeCanvases(canvases, mode)`
```javascript
const merged = CanvasUtils.mergeCanvases([canvas1, canvas2], 'horizontal');
```

#### `getDominantColor(canvas)`
```javascript
const color = CanvasUtils.getDominantColor(canvas);
// Returns: "#FF6B9D"
```

#### `imageToCanvas(source)`
```javascript
const canvas = await CanvasUtils.imageToCanvas('path/to/image.png');
```

#### `getCanvasFileSize(canvas, format, quality)`
```javascript
const size = await CanvasUtils.getCanvasFileSize(canvas, 'png', 1);
console.log(CanvasUtils.formatFileSize(size)); // "85.4 KB"
```

---

## 💡 Usage Examples

### Example 1: Download Avatar as PNG
```javascript
const handleDownload = () => {
    if (!sceneRef.current) return;
    
    const dataUrl = sceneRef.current.exportAsBase64();
    const link = document.createElement('a');
    link.download = 'avatar.png';
    link.href = dataUrl;
    link.click();
};
```

### Example 2: Upload to Server
```javascript
const handleUpload = async () => {
    const blob = await sceneRef.current.exportAsBlob('jpeg', 0.9);
    
    const formData = new FormData();
    formData.append('avatar', blob, 'avatar.jpg');
    
    await fetch('/api/upload-avatar', {
        method: 'POST',
        body: formData
    });
};
```

### Example 3: Save Multiple Sizes
```javascript
const saveSizes = () => {
    // Original
    const original = sceneRef.current.exportAsBase64();
    
    // Thumbnail
    const thumbnail = sceneRef.current.createThumbnail(150, 150);
    
    // HD
    const hd = sceneRef.current.exportAtResolution(1920, 1080);
    
    // Save all versions
    localStorage.setItem('avatar_original', original);
    localStorage.setItem('avatar_thumbnail', thumbnail);
    localStorage.setItem('avatar_hd', hd);
};
```

### Example 4: Export with Custom Background
```javascript
const exportForPrint = () => {
    // Add white background for printing
    const dataUrl = sceneRef.current.exportWithBackground('#FFFFFF');
    
    // Download as high-quality JPEG
    const link = document.createElement('a');
    link.download = 'avatar-print.jpg';
    link.href = dataUrl;
    link.click();
};
```

### Example 5: Create Avatar Strip
```javascript
import { mergeCanvases } from './utils/canvasUtils';

const createAvatarStrip = async () => {
    // Export multiple variants
    const variants = [
        sceneRef.current.exportAsBase64(),
        // ... change avatar settings ...
        sceneRef.current.exportAsBase64(),
        // ... change again ...
        sceneRef.current.exportAsBase64()
    ];
    
    // Convert to canvases
    const canvases = await Promise.all(
        variants.map(url => CanvasUtils.imageToCanvas(url))
    );
    
    // Merge horizontally
    const strip = mergeCanvases(canvases, 'horizontal');
    CanvasUtils.downloadCanvas(strip, 'avatar-strip.png');
};
```

### Example 6: Social Media Share
```javascript
const shareOnSocialMedia = async () => {
    if (!navigator.share) {
        alert('Sharing not supported');
        return;
    }
    
    const blob = await sceneRef.current.exportAsBlob('png', 1);
    const file = new File([blob], 'avatar.png', { type: 'image/png' });
    
    await navigator.share({
        title: 'My Avatar',
        text: 'Check out my cool avatar!',
        files: [file]
    });
};
```

### Example 7: Apply Instagram-style Filter
```javascript
import { applyFilterToCanvas } from './utils/canvasUtils';

const applyVintageFilter = () => {
    const canvas = sceneRef.current.game.canvas;
    const filtered = applyFilterToCanvas(
        canvas,
        'sepia(50%) contrast(120%) brightness(90%)'
    );
    CanvasUtils.downloadCanvas(filtered, 'avatar-vintage.png');
};
```

---

## 🌐 Browser Compatibility

### Core Canvas Features
✅ **Supported by all modern browsers:**
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Clipboard API
✅ **Copy to Clipboard:**
- Chrome 76+
- Firefox 87+
- Safari 13.1+
- Edge 79+

⚠️ **Requires HTTPS** (except localhost)

### Web Share API
✅ **Social Sharing:**
- Chrome Mobile 89+
- Safari Mobile 12.2+
- Samsung Internet 11+

❌ **Not Available:**
- Desktop browsers (except Safari macOS)

### Canvas Blob
✅ **Universal Support:**
- All modern browsers
- IE 10+ (with polyfill)

---

## 📊 File Size Comparison

Typical avatar export sizes (400x500px):

| Format | Quality | Size | Use Case |
|--------|---------|------|----------|
| PNG | Lossless | ~85 KB | Default, web display |
| JPEG | 95% | ~45 KB | Smaller, no transparency |
| JPEG | 80% | ~25 KB | Email, mobile |
| PNG Thumbnail 200x200 | Lossless | ~25 KB | Icons, previews |
| PNG HD 800x1000 | Lossless | ~180 KB | High resolution, print |

---

## 🔒 Security & Privacy

### CORS Considerations
When loading external images:
```javascript
img.crossOrigin = 'anonymous';
```

### Clipboard Permissions
Browser will prompt user for clipboard access on first use.

### Local Storage
Snapshots saved to localStorage:
- Max ~5-10 MB total
- Persists between sessions
- User can clear via browser settings

---

## 🎯 Best Practices

### 1. Optimize Quality Settings
```javascript
// Web display
exportAsJPEG(0.85) // Good balance

// Thumbnails
createThumbnail(200, 200) // Small size

// Print/HD
exportAsBase64(1) // Maximum quality
```

### 2. Handle Errors
```javascript
try {
    const success = await sceneRef.current.copyToClipboard();
    if (success) {
        showNotification('Copied!');
    }
} catch (error) {
    showNotification('Copy failed. Try downloading instead.');
}
```

### 3. Show Progress
```javascript
const exportLarge = async () => {
    showLoading(true);
    const hd = sceneRef.current.exportAtResolution(3840, 2160);
    await downloadImage(hd);
    showLoading(false);
};
```

### 4. Cleanup
```javascript
// When component unmounts
useEffect(() => {
    return () => {
        if (gameInstanceRef.current) {
            gameInstanceRef.current.destroy(true);
        }
    };
}, []);
```

---

## 🚀 Advanced Features

### Custom Export Pipeline
```javascript
const customExport = async () => {
    // 1. Get canvas
    const canvas = sceneRef.current.game.canvas;
    
    // 2. Add background
    const withBg = CanvasUtils.addBackgroundToCanvas(canvas, '#F0F0F0');
    
    // 3. Apply filter
    const filtered = CanvasUtils.applyFilterToCanvas(withBg, 'brightness(110%)');
    
    // 4. Resize
    const resized = CanvasUtils.resizeCanvas(filtered, 1200, 1500);
    
    // 5. Download
    CanvasUtils.downloadCanvas(resized, 'custom-avatar.png');
};
```

### Watermark Addition
```javascript
const addWatermark = () => {
    const ctx = sceneRef.current.getCanvasContext();
    ctx.font = '20px Arial';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.fillText('© MyApp', 10, canvas.height - 10);
};
```

---

## 📚 Related Documentation

- [AVATAR_QUICKSTART.md](AVATAR_QUICKSTART.md) - Quick start guide
- [AVATAR_PANEL_README.md](AVATAR_PANEL_README.md) - Full panel documentation
- [MDN Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [Phaser 3 Documentation](https://photonstorm.github.io/phaser3-docs/)

---

**Enjoy the canvas features!** 🎨✨
