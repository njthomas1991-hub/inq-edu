/**
 * Canvas Utilities - Helper functions for canvas manipulation and export
 * 
 * Provides utility functions for working with HTML5 Canvas elements,
 * including export, manipulation, and image processing.
 */

/**
 * Download a canvas as an image file
 * @param {HTMLCanvasElement} canvas - The canvas element
 * @param {string} filename - Desired filename
 * @param {string} format - 'png' or 'jpeg'
 * @param {number} quality - Quality from 0 to 1
 */
export function downloadCanvas(canvas, filename = 'image.png', format = 'png', quality = 1) {
    const mimeType = format === 'jpeg' ? 'image/jpeg' : 'image/png';
    const dataUrl = canvas.toDataURL(mimeType, quality);
    
    const link = document.createElement('a');
    link.download = filename;
    link.href = dataUrl;
    link.click();
}

/**
 * Convert canvas to Blob
 * @param {HTMLCanvasElement} canvas - The canvas element
 * @param {string} format - 'png' or 'jpeg'
 * @param {number} quality - Quality from 0 to 1
 * @returns {Promise<Blob>}
 */
export function canvasToBlob(canvas, format = 'png', quality = 1) {
    return new Promise((resolve) => {
        const mimeType = format === 'jpeg' ? 'image/jpeg' : 'image/png';
        canvas.toBlob((blob) => {
            resolve(blob);
        }, mimeType, quality);
    });
}

/**
 * Copy canvas to clipboard
 * @param {HTMLCanvasElement} canvas - The canvas element
 * @returns {Promise<boolean>} Success status
 */
export async function copyCanvasToClipboard(canvas) {
    try {
        const blob = await canvasToBlob(canvas, 'png', 1);
        const item = new ClipboardItem({ 'image/png': blob });
        await navigator.clipboard.write([item]);
        return true;
    } catch (err) {
        console.error('Failed to copy to clipboard:', err);
        return false;
    }
}

/**
 * Resize canvas maintaining aspect ratio
 * @param {HTMLCanvasElement} sourceCanvas - Source canvas
 * @param {number} maxWidth - Maximum width
 * @param {number} maxHeight - Maximum height
 * @returns {HTMLCanvasElement} Resized canvas
 */
export function resizeCanvas(sourceCanvas, maxWidth, maxHeight) {
    const tempCanvas = document.createElement('canvas');
    
    let width = sourceCanvas.width;
    let height = sourceCanvas.height;
    const ratio = Math.min(maxWidth / width, maxHeight / height);
    
    width = width * ratio;
    height = height * ratio;
    
    tempCanvas.width = width;
    tempCanvas.height = height;
    
    const ctx = tempCanvas.getContext('2d');
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(sourceCanvas, 0, 0, width, height);
    
    return tempCanvas;
}

/**
 * Add background color to canvas
 * @param {HTMLCanvasElement} sourceCanvas - Source canvas
 * @param {string} backgroundColor - Hex color code
 * @returns {HTMLCanvasElement} Canvas with background
 */
export function addBackgroundToCanvas(sourceCanvas, backgroundColor = '#FFFFFF') {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = sourceCanvas.width;
    tempCanvas.height = sourceCanvas.height;
    
    const ctx = tempCanvas.getContext('2d');
    
    // Fill background
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // Draw original canvas on top
    ctx.drawImage(sourceCanvas, 0, 0);
    
    return tempCanvas;
}

/**
 * Crop canvas to specific region
 * @param {HTMLCanvasElement} sourceCanvas - Source canvas
 * @param {Object} rect - {x, y, width, height}
 * @returns {HTMLCanvasElement} Cropped canvas
 */
export function cropCanvas(sourceCanvas, rect) {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = rect.width;
    tempCanvas.height = rect.height;
    
    const ctx = tempCanvas.getContext('2d');
    ctx.drawImage(
        sourceCanvas,
        rect.x, rect.y, rect.width, rect.height,
        0, 0, rect.width, rect.height
    );
    
    return tempCanvas;
}

/**
 * Apply filter to canvas
 * @param {HTMLCanvasElement} sourceCanvas - Source canvas
 * @param {string} filter - CSS filter string (e.g., 'grayscale(100%)')
 * @returns {HTMLCanvasElement} Filtered canvas
 */
export function applyFilterToCanvas(sourceCanvas, filter) {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = sourceCanvas.width;
    tempCanvas.height = sourceCanvas.height;
    
    const ctx = tempCanvas.getContext('2d');
    ctx.filter = filter;
    ctx.drawImage(sourceCanvas, 0, 0);
    
    return tempCanvas;
}

/**
 * Merge multiple canvases
 * @param {Array<HTMLCanvasElement>} canvases - Array of canvas elements
 * @param {string} mode - 'horizontal' or 'vertical'
 * @returns {HTMLCanvasElement} Merged canvas
 */
export function mergeCanvases(canvases, mode = 'horizontal') {
    if (!canvases || canvases.length === 0) return null;
    
    const tempCanvas = document.createElement('canvas');
    
    if (mode === 'horizontal') {
        tempCanvas.width = canvases.reduce((sum, c) => sum + c.width, 0);
        tempCanvas.height = Math.max(...canvases.map(c => c.height));
        
        const ctx = tempCanvas.getContext('2d');
        let xOffset = 0;
        
        canvases.forEach(canvas => {
            ctx.drawImage(canvas, xOffset, 0);
            xOffset += canvas.width;
        });
    } else {
        tempCanvas.width = Math.max(...canvases.map(c => c.width));
        tempCanvas.height = canvases.reduce((sum, c) => sum + c.height, 0);
        
        const ctx = tempCanvas.getContext('2d');
        let yOffset = 0;
        
        canvases.forEach(canvas => {
            ctx.drawImage(canvas, 0, yOffset);
            yOffset += canvas.height;
        });
    }
    
    return tempCanvas;
}

/**
 * Get dominant color from canvas
 * @param {HTMLCanvasElement} canvas - The canvas element
 * @returns {string} Hex color code
 */
export function getDominantColor(canvas) {
    const ctx = canvas.getContext('2d');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    const colorCount = {};
    let maxCount = 0;
    let dominantColor = '#000000';
    
    // Sample every 10th pixel for performance
    for (let i = 0; i < data.length; i += 40) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        const a = data[i + 3];
        
        // Skip transparent pixels
        if (a < 128) continue;
        
        const color = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
        
        colorCount[color] = (colorCount[color] || 0) + 1;
        
        if (colorCount[color] > maxCount) {
            maxCount = colorCount[color];
            dominantColor = color;
        }
    }
    
    return dominantColor;
}

/**
 * Convert image to canvas
 * @param {HTMLImageElement|string} source - Image element or URL
 * @returns {Promise<HTMLCanvasElement>}
 */
export function imageToCanvas(source) {
    return new Promise((resolve, reject) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        if (typeof source === 'string') {
            const img = new Image();
            img.crossOrigin = 'anonymous';
            img.onload = () => {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                resolve(canvas);
            };
            img.onerror = reject;
            img.src = source;
        } else {
            canvas.width = source.width;
            canvas.height = source.height;
            ctx.drawImage(source, 0, 0);
            resolve(canvas);
        }
    });
}

/**
 * Create thumbnail from canvas
 * @param {HTMLCanvasElement} sourceCanvas - Source canvas
 * @param {number} size - Thumbnail size (width/height)
 * @returns {HTMLCanvasElement} Thumbnail canvas
 */
export function createThumbnail(sourceCanvas, size = 200) {
    return resizeCanvas(sourceCanvas, size, size);
}

/**
 * Check if clipboard API is available
 * @returns {boolean}
 */
export function isClipboardAvailable() {
    return !!(navigator.clipboard && navigator.clipboard.write);
}

/**
 * Get canvas file size estimate
 * @param {HTMLCanvasElement} canvas - The canvas element
 * @param {string} format - 'png' or 'jpeg'
 * @param {number} quality - Quality from 0 to 1
 * @returns {Promise<number>} Size in bytes
 */
export async function getCanvasFileSize(canvas, format = 'png', quality = 1) {
    const blob = await canvasToBlob(canvas, format, quality);
    return blob.size;
}

/**
 * Format file size for display
 * @param {number} bytes - Size in bytes
 * @returns {string} Formatted string (e.g., "2.5 MB")
 */
export function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

export default {
    downloadCanvas,
    canvasToBlob,
    copyCanvasToClipboard,
    resizeCanvas,
    addBackgroundToCanvas,
    cropCanvas,
    applyFilterToCanvas,
    mergeCanvases,
    getDominantColor,
    imageToCanvas,
    createThumbnail,
    isClipboardAvailable,
    getCanvasFileSize,
    formatFileSize
};
