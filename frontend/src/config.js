// Frontend configuration
const resolveApiBaseUrl = () => {
  if (typeof import.meta !== 'undefined' && import.meta.env) {
    return (
      import.meta.env.VITE_API_URL ||
      import.meta.env.VITE_API_BASE_URL ||
      'http://127.0.0.1:8000/api'
    );
  }

  if (typeof process !== 'undefined' && process.env) {
    return process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';
  }

  return 'http://127.0.0.1:8000/api';
};

const config = {
  API_BASE_URL: resolveApiBaseUrl(),

  // Phaser game configuration
  PHASER_CONFIG: {
    width: 800,
    height: 600,
    parent: 'game-container',
    physics: {
      default: 'arcade',
      arcade: {
        gravity: { y: 300 },
        debug: false
      }
    }
  }
};

export default config;
