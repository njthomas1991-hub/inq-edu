import React from 'react';
import '../css/MonsterAvatar.css';

const MonsterAvatar = ({ avatar }) => {
  if (!avatar) return null;
  return (
    <div className="monster-avatar">
      {/* Simplified avatar rendering placeholder */}
      <div className="monster-body" style={{ background: avatar.primaryColor }} />
    </div>
  );
};

export default MonsterAvatar;
