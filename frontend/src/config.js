// Frontend configuration
const config = {
  // API base URL
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api',
  
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
