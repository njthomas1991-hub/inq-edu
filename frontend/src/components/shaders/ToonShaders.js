/**
 * Stylized Shaders for Avatar3D
 * Provides cartoon/toon shading and other artistic rendering effects
 */

import * as THREE from 'three';

/**
 * Toon/Cartoon Shader Material
 * Creates a stylized, hand-drawn appearance with color banding and outlines
 */
export const createToonMaterial = (baseColor, options = {}) => {
  const material = new THREE.ShaderMaterial({
    uniforms: {
      uColor: { value: new THREE.Color(baseColor) },
      uLightPos: { value: new THREE.Vector3(5, 5, 5) },
      uBands: { value: options.bands || 3 },
      uOutlineSize: { value: options.outlineSize || 0.05 },
      uSpecularPower: { value: options.specularPower || 32 },
    },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec3 vViewDir;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = (modelMatrix * vec4(position, 1.0)).xyz;
        vViewDir = normalize((cameraPosition - vPosition));
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform vec3 uColor;
      uniform vec3 uLightPos;
      uniform float uBands;
      uniform float uOutlineSize;
      uniform float uSpecularPower;
      
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec3 vViewDir;
      
      float quantize(float value, float levels) {
        return floor(value * levels) / levels;
      }
      
      void main() {
        vec3 lightDir = normalize(uLightPos - vPosition);
        vec3 normal = normalize(vNormal);
        
        // Base diffuse with quantization for toon effect
        float diffuse = dot(normal, lightDir);
        diffuse = max(0.0, diffuse);
        diffuse = quantize(diffuse, uBands);
        
        // Specular highlight
        vec3 reflection = reflect(-lightDir, normal);
        float specular = pow(max(0.0, dot(vViewDir, reflection)), uSpecularPower);
        specular = step(0.5, specular);
        
        // Rim light for cartoon effect
        float rim = 1.0 - dot(vViewDir, normal);
        rim = smoothstep(0.0, 1.0, rim);
        rim *= 0.3;
        
        // Edge detection outline
        vec3 edgeNormal = vNormal;
        float edge = dot(vViewDir, edgeNormal);
        edge = step(0.3, edge);
        
        // Combine effects
        vec3 finalColor = uColor * (0.3 + diffuse * 0.7);
        finalColor += vec3(specular) * 0.5;
        finalColor += vec3(rim);
        
        gl_FragColor = vec4(finalColor, 1.0);
      }
    `,
    side: THREE.FrontSide,
  });
  
  return material;
};

/**
 * Cell Shading / Comic Book Shader
 * Creates bold outlines with limited color palette
 */
export const createCellShadeMaterial = (baseColor, options = {}) => {
  const material = new THREE.ShaderMaterial({
    uniforms: {
      uColor: { value: new THREE.Color(baseColor) },
      uDarkColor: { value: new THREE.Color(options.darkColor || 0x1a1a1a) },
      uLightColor: { value: new THREE.Color(options.lightColor || 0xffffff) },
      uLightPos: { value: new THREE.Vector3(5, 5, 5) },
      uCellSize: { value: options.cellSize || 3 },
    },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = (modelMatrix * vec4(position, 1.0)).xyz;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform vec3 uColor;
      uniform vec3 uDarkColor;
      uniform vec3 uLightColor;
      uniform vec3 uLightPos;
      uniform float uCellSize;
      
      varying vec3 vNormal;
      varying vec3 vPosition;
      
      void main() {
        vec3 lightDir = normalize(uLightPos - vPosition);
        vec3 normal = normalize(vNormal);
        
        // Cell shading with limited steps
        float intensity = dot(normal, lightDir);
        intensity = max(0.0, intensity);
        
        // Posterize effect
        intensity = floor(intensity * uCellSize) / uCellSize;
        
        vec3 finalColor;
        if (intensity > 0.666) {
          finalColor = mix(uColor, uLightColor, 0.3);
        } else if (intensity > 0.333) {
          finalColor = uColor;
        } else {
          finalColor = mix(uColor, uDarkColor, 0.5);
        }
        
        gl_FragColor = vec4(finalColor, 1.0);
      }
    `,
    side: THREE.FrontSide,
  });
  
  return material;
};

/**
 * Watercolor/Artistic Shader
 * Creates soft, artistic appearance with color gradients
 */
export const createWatercolorMaterial = (baseColor, options = {}) => {
  const material = new THREE.ShaderMaterial({
    uniforms: {
      uColor: { value: new THREE.Color(baseColor) },
      uWaterDensity: { value: options.waterDensity || 0.7 },
      uTime: { value: 0 },
    },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = (modelMatrix * vec4(position, 1.0)).xyz;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform vec3 uColor;
      uniform float uWaterDensity;
      uniform float uTime;
      
      varying vec3 vNormal;
      varying vec3 vPosition;
      
      float noise(vec3 p) {
        return fract(sin(dot(p, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
      }
      
      void main() {
        vec3 normal = normalize(vNormal);
        
        // Soft gradient based on normal direction
        float gradient = (normal.y + 1.0) * 0.5;
        
        // Add subtle noise for watercolor effect
        float n = noise(vPosition * 3.0 + uTime * 0.1);
        gradient += (n - 0.5) * uWaterDensity;
        
        graduation = clamp(gradient, 0.3, 1.0);
        
        vec3 finalColor = mix(uColor * 0.5, uColor, gradient);
        
        gl_FragColor = vec4(finalColor, 1.0);
      }
    `,
    side: THREE.FrontSide,
  });
  
  return material;
};

/**
 * Outline Pass for Toon Shading
 * Renders a black outline around the character
 */
export class OutlinePass {
  constructor(scene, camera, renderer) {
    this.scene = scene;
    this.camera = camera;
    this.renderer = renderer;
    this.outlineRenderTarget = new THREE.WebGLRenderTarget(
      renderer.domElement.width,
      renderer.domElement.height
    );
  }

  render() {
    // Save current scene state
    const originalBackground = this.scene.background;
    const originalFogColor = this.scene.fog ? this.scene.fog.color : null;
    
    // Render outline to texture
    this.renderer.setRenderTarget(this.outlineRenderTarget);
    this.renderer.setClearColor(0xffffff, 1);
    this.renderer.clear();
    
    // Apply outline shader to all objects
    this.scene.traverse((child) => {
      if (child.isMesh) {
        child.material = this.createOutlineShader(child.material);
      }
    });
    
    this.renderer.render(this.scene, this.camera);
    
    // Restore original state
    this.renderer.setRenderTarget(null);
    this.renderer.setClearColor(originalBackground, 1);
    this.scene.background = originalBackground;
  }

  createOutlineShader(originalMaterial) {
    return new THREE.MeshBasicMaterial({
      color: 0x000000,
      side: THREE.BackSide,
    });
  }
}

/**
 * Create stylized lighting setup for cartoon appearance
 */
export const createStylizedLighting = (scene) => {
  // Remove default lights
  scene.children.forEach((child) => {
    if (child.isLight) {
      scene.remove(child);
    }
  });

  // Key light - harsh for clearly defined shadows
  const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
  keyLight.position.set(10, 10, 5);
  keyLight.shadow.mapSize.width = 2048;
  keyLight.shadow.mapSize.height = 2048;
  keyLight.castShadow = true;
  scene.add(keyLight);

  // Fill light - from opposite side, softer
  const fillLight = new THREE.DirectionalLight(0x6699ff, 0.5);
  fillLight.position.set(-10, 5, -10);
  scene.add(fillLight);

  // Rim light - behind for silhouette effect
  const rimLight = new THREE.DirectionalLight(0xffaa44, 0.4);
  rimLight.position.set(0, 5, -15);
  scene.add(rimLight);

  // Ambient for overall illumination
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);

  return { keyLight, fillLight, rimLight, ambientLight };
};

/**
 * Apply shader to mesh recursively
 */
export const applyShaderToMesh = (mesh, shaderMaterial) => {
  if (mesh.isMesh) {
    mesh.material = shaderMaterial;
  }
  
  mesh.children.forEach((child) => {
    applyShaderToMesh(child, shaderMaterial);
  });
};

/**
 * Create post-processing effects for stylization
 */
export const createPostProcessingEffects = (composer, camera) => {
  // FXAAShader - anti-aliasing
  const { FXAAShader } = require('three/examples/jsm/shaders/FXAAShader');
  const fxaaPass = new THREE.ShaderPass(FXAAShader);
  fxaaPass.uniforms['resolution'].value.x = 1 / window.innerWidth;
  fxaaPass.uniforms['resolution'].value.y = 1 / window.innerHeight;
  composer.addPass(fxaaPass);

  return { fxaaPass };
};

export default {
  createToonMaterial,
  createCellShadeMaterial,
  createWatercolorMaterial,
  createStylizedLighting,
  applyShaderToMesh,
  createPostProcessingEffects,
  OutlinePass,
};
