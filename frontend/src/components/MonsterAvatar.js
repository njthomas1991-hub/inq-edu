import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import * as PIXI from 'pixi.js';
import './MonsterAvatar.css';

/**
 * MonsterAvatar Component
 * 
 * Renders a PixiJS-based monster avatar from sprite parts
 * Creates a "living" effect with animations
 */
const MonsterAvatar = ({ 
  avatar = null, 
  width = 300, 
  height = 300,
  onLoad = null 
}) => {
  const containerRef = useRef(null);
  const appRef = useRef(null);
  const monsterRef = useRef(null);

  // Color mapping for avatar parts
  const getColor = (colorHex) => {
    return parseInt(colorHex.replace('#', ''), 16);
  };

  // Create placeholder graphics when assets aren't available
  const createBodyGraphic = (color) => {
    const graphics = new PIXI.Graphics();
    graphics.beginFill(color);
    graphics.drawCircle(0, 0, 40);
    graphics.endFill();
    return graphics;
  };

  const createEyeGraphic = () => {
    const graphics = new PIXI.Graphics();
    // Outer eye
    graphics.beginFill(0xFFFFFF);
    graphics.drawCircle(0, 0, 12);
    graphics.endFill();
    // Pupil
    graphics.beginFill(0x000000);
    graphics.drawCircle(0, 0, 6);
    graphics.endFill();
    // Shine effect
    graphics.beginFill(0xFFFFFF);
    graphics.drawCircle(-2, -2, 2);
    graphics.endFill();
    return graphics;
  };

  const createMouthGraphic = (type) => {
    const graphics = new PIXI.Graphics();
    graphics.lineStyle(2, 0x000000);
    
    switch (type) {
      case 'smile':
        graphics.arc(0, 0, 10, Math.PI, 0);
        break;
      case 'grin':
        graphics.arc(0, 0, 15, Math.PI, 0);
        break;
      case 'open':
        graphics.beginFill(0xFF69B4);
        graphics.drawEllipse(0, 5, 8, 12);
        graphics.endFill();
        graphics.lineStyle(2, 0x000000);
        graphics.drawEllipse(0, 5, 8, 12);
        break;
      case 'neutral':
        graphics.moveTo(-8, 0);
        graphics.lineTo(8, 0);
        break;
      default:
        graphics.arc(0, 0, 10, Math.PI, 0);
    }
    
    return graphics;
  };

  const createAccessoryGraphic = (type) => {
    if (type === 'none') return null;

    const graphics = new PIXI.Graphics();
    
    switch (type) {
      case 'cap':
        graphics.beginFill(0xFF0000);
        graphics.moveTo(-30, -40);
        graphics.lineTo(30, -40);
        graphics.lineTo(20, -50);
        graphics.lineTo(-20, -50);
        graphics.closePath();
        graphics.endFill();
        break;
      case 'hat':
        graphics.beginFill(0x8B4513);
        graphics.moveTo(-40, -45);
        graphics.lineTo(40, -45);
        graphics.lineTo(35, -65);
        graphics.lineTo(-35, -65);
        graphics.closePath();
        graphics.endFill();
        break;
      case 'crown':
        graphics.beginFill(0xFFD700);
        graphics.drawStar(0, -50, 5, 20, 15);
        graphics.endFill();
        graphics.beginFill(0xFF0000);
        for (let i = 0; i < 5; i++) {
          graphics.drawCircle(
            Math.cos(i * Math.PI * 2 / 5) * 15, 
            -50 + Math.sin(i * Math.PI * 2 / 5) * 15, 
            3
          );
        }
        graphics.endFill();
        break;
      case 'glasses':
        graphics.lineStyle(3, 0x000000);
        graphics.drawCircle(-10, -5, 8);
        graphics.drawCircle(10, -5, 8);
        graphics.moveTo(0, -5);
        graphics.lineTo(0, -5);
        break;
      default:
        return null;
    }
    
    return graphics;
  };

  useEffect(() => {
    if (!containerRef.current) return;

    // Initialize PIXI Application
    const app = new PIXI.Application({
      width,
      height,
      backgroundAlpha: 0,
      antialias: true,
      resolution: window.devicePixelRatio || 1,
    });

    containerRef.current.appendChild(app.view);
    appRef.current = app;

    // Create monster container
    const monster = new PIXI.Container();
    monster.x = width / 2;
    monster.y = height / 2;
    app.stage.addChild(monster);
    monsterRef.current = monster;

    // Create avatar parts
    const primaryColor = avatar?.primaryColor 
      ? getColor(avatar.primaryColor) 
      : getColor('#FF6B9D');
    const accentColor = avatar?.accentColor 
      ? getColor(avatar.accentColor) 
      : getColor('#FFB347');

    // Body
    const body = createBodyGraphic(primaryColor);
    body.y = 5;

    // Eyes
    const eyesContainer = new PIXI.Container();
    eyesContainer.y = -15;

    const leftEye = createEyeGraphic(0xFFFFFF);
    leftEye.x = -15;
    eyesContainer.addChild(leftEye);

    const rightEye = createEyeGraphic(0xFFFFFF);
    rightEye.x = 15;
    eyesContainer.addChild(rightEye);

    // Mouth
    const mouth = createMouthGraphic(avatar?.mouthType || 'smile');
    mouth.y = 20;

    // Arms
    const armsContainer = new PIXI.Container();
    const leftArm = new PIXI.Graphics();
    leftArm.beginFill(accentColor);
    leftArm.drawCircle(0, 0, 8);
    leftArm.endFill();
    leftArm.x = -50;
    leftArm.y = 0;
    armsContainer.addChild(leftArm);

    const rightArm = new PIXI.Graphics();
    rightArm.beginFill(accentColor);
    rightArm.drawCircle(0, 0, 8);
    rightArm.endFill();
    rightArm.x = 50;
    rightArm.y = 0;
    armsContainer.addChild(rightArm);

    // Accessory
    const accessory = createAccessoryGraphic(avatar?.accessory || 'none');

    // Add all parts to monster
    monster.addChild(body, eyesContainer, mouth, armsContainer);
    if (accessory) {
      monster.addChild(accessory);
    }

    // Animation: "alive" effect
    let time = 0;
    app.ticker.add(() => {
      time += 0.01;

      // Breathing/bouncing effect
      monster.scale.y = 1 + Math.sin(time * 2) * 0.03;
      monster.rotation = Math.sin(time * 1.5) * 0.02;

      // Eyes blinking
      const blinkCycle = (Math.sin(time * 0.5) + 1) / 2;
      if (blinkCycle > 0.9 || blinkCycle < 0.1) {
        eyesContainer.scale.y = 0.1;
      } else {
        eyesContainer.scale.y = 1;
      }

      // Arms wave
      leftArm.rotation = Math.sin(time * 1.5) * 0.4 - 0.2;
      rightArm.rotation = Math.sin(time * 1.5 + Math.PI) * 0.4 + 0.2;
    });

    if (onLoad) onLoad();

    // Cleanup
    return () => {
      if (containerRef.current && app.view.parentElement === containerRef.current) {
        containerRef.current.removeChild(app.view);
      }
      app.destroy(true);
    };
  }, [avatar, width, height, onLoad]);

  return (
    <div className="monster-avatar-container" ref={containerRef} />
  );
};

MonsterAvatar.propTypes = {
  avatar: PropTypes.shape({
    primaryColor: PropTypes.string,
    accentColor: PropTypes.string,
    mouthType: PropTypes.string,
    accessory: PropTypes.string,
  }),
  width: PropTypes.number,
  height: PropTypes.number,
  onLoad: PropTypes.func,
};

export default MonsterAvatar;
