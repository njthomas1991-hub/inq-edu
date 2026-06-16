import React, { useEffect, useMemo, useState } from 'react';
import PropTypes from 'prop-types';
import './MonsterAvatar.css';

/**
 * MonsterAvatar Component
 * 
 * Renders a lightweight SVG-based monster avatar from sprite parts.
 */
const MonsterAvatar = ({ 
  avatar = null, 
  width = 300, 
  height = 300,
  onLoad = null 
}) => {
  const [pulse, setPulse] = useState(false);

  const styles = useMemo(() => ({
    width,
    height,
    '--monster-primary': avatar?.primaryColor || '#FF6B9D',
    '--monster-accent': avatar?.accentColor || '#FFB347',
  }), [avatar?.accentColor, avatar?.primaryColor, height, width]);

  useEffect(() => {
    if (onLoad) onLoad();
  }, [avatar, width, height, onLoad]);

  return (
    <div className="monster-avatar-container" style={styles}>
      <svg
        viewBox="0 0 240 240"
        width={width}
        height={height}
        role="img"
        aria-label="Monster avatar preview"
      >
        <defs>
          <radialGradient id="monsterGlow" cx="50%" cy="40%" r="70%">
            <stop offset="0%" stopColor="rgba(255,255,255,0.55)" />
            <stop offset="100%" stopColor="rgba(255,255,255,0)" />
          </radialGradient>
        </defs>

        <circle cx="120" cy="120" r="92" fill="url(#monsterGlow)" />
        <g className={pulse ? 'monster-avatar pulse' : 'monster-avatar'}>
          <ellipse cx="120" cy="126" rx="68" ry="72" fill="var(--monster-primary)" />
          <circle cx="92" cy="104" r="14" fill="#fff" />
          <circle cx="148" cy="104" r="14" fill="#fff" />
          <circle cx="92" cy="104" r="7" fill="#111827" />
          <circle cx="148" cy="104" r="7" fill="#111827" />
          <circle cx="88" cy="100" r="2.5" fill="#fff" />
          <circle cx="144" cy="100" r="2.5" fill="#fff" />

          {avatar?.mouthType === 'open' ? (
            <ellipse cx="120" cy="150" rx="11" ry="15" fill="#111827" />
          ) : avatar?.mouthType === 'neutral' ? (
            <line x1="108" y1="151" x2="132" y2="151" stroke="#111827" strokeWidth="4" strokeLinecap="round" />
          ) : avatar?.mouthType === 'grin' ? (
            <path d="M102 146 Q120 166 138 146" fill="none" stroke="#111827" strokeWidth="4" strokeLinecap="round" />
          ) : (
            <path d="M104 146 Q120 160 136 146" fill="none" stroke="#111827" strokeWidth="4" strokeLinecap="round" />
          )}

          <path d="M52 136 Q26 124 34 104" fill="none" stroke="var(--monster-accent)" strokeWidth="8" strokeLinecap="round" />
          <path d="M188 136 Q214 124 206 104" fill="none" stroke="var(--monster-accent)" strokeWidth="8" strokeLinecap="round" />
          <circle cx="52" cy="136" r="8" fill="var(--monster-accent)" />
          <circle cx="188" cy="136" r="8" fill="var(--monster-accent)" />

          {avatar?.accessory === 'crown' && (
            <path d="M84 68 L98 50 L120 68 L142 50 L156 68 L150 78 L90 78 Z" fill="#facc15" />
          )}
          {avatar?.accessory === 'hat' && (
            <path d="M70 72 H170 L160 56 H80 Z" fill="#92400e" />
          )}
          {avatar?.accessory === 'cap' && (
            <path d="M78 74 H162 L152 58 H88 Z" fill="#ef4444" />
          )}
          {avatar?.accessory === 'glasses' && (
            <g fill="none" stroke="#111827" strokeWidth="4">
              <circle cx="94" cy="103" r="16" />
              <circle cx="146" cy="103" r="16" />
              <path d="M110 103 H130" />
            </g>
          )}
        </g>
      </svg>
    </div>
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
