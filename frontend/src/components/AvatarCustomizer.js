import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import MonsterAvatar from './MonsterAvatar';
import './AvatarCustomizer.css';

/**
 * AvatarCustomizer Component
 * 
 * Allows users to customize their monster avatar
 * Real-time preview with save functionality
 */
const AvatarCustomizer = ({ onSave = null }) => {
  const [avatar, setAvatar] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const bodyTypes = ['round_blue', 'round_pink', 'round_green', 'round_yellow', 'square_purple', 'square_orange'];
  const eyeTypes = ['big_happy', 'big_sleepy', 'small_angry', 'round_confused', 'star_sparkly'];
  const mouthTypes = ['smile', 'grin', 'open', 'neutral', 'tongue'];
  const accessories = ['none', 'cap', 'hat', 'crown', 'glasses', 'bow'];

  // Load avatar data on component mount
  useEffect(() => {
    const loadAvatar = async () => {
      try {
        const response = await fetch('/api/avatar/');
        const data = await response.json();
        if (data.success && data.avatar) {
          setAvatar(data.avatar);
        }
        setLoading(false);
      } catch (error) {
        console.error('Error loading avatar:', error);
        // Create default avatar
        setAvatar({
          bodyType: 'round_blue',
          eyeType: 'big_happy',
          mouthType: 'smile',
          accessory: 'none',
          primaryColor: '#FF6B9D',
          accentColor: '#FFB347',
        });
        setLoading(false);
      }
    };

    loadAvatar();
  }, []);

  const updateAvatar = (field, value) => {
    setAvatar(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');

    try {
      const response = await fetch('/api/avatar/save/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
        },
        body: JSON.stringify(avatar),
      });

      const data = await response.json();

      if (data.success) {
        setMessage('✓ Avatar saved successfully!');
        if (onSave) onSave(avatar);

        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('✗ Error saving avatar: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      setMessage('✗ Error saving avatar: ' + error.message);
    } finally {
      setSaving(false);
    }
  };

  const handleRandomize = async () => {
    try {
      const response = await fetch('/api/avatar/randomize/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (data.success && data.avatar) {
        setAvatar(data.avatar);
        setMessage('🎲 Avatar randomized!');
        setTimeout(() => setMessage(''), 2000);
      }
    } catch (error) {
      console.error('Error randomizing avatar:', error);
    }
  };

  if (loading) {
    return <div className="avatar-customizer">Loading...</div>;
  }

  if (!avatar) {
    return <div className="avatar-customizer">Error loading avatar</div>;
  }

  return (
    <div className="avatar-customizer">
      <h2>🧟 Customize Your Monster</h2>

      <div className="customizer-content">
        {/* Preview */}
        <div className="preview-section">
          <MonsterAvatar avatar={avatar} width={300} height={300} />
          {message && (
            <div className={`message ${message.includes('✓') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="controls-section">
          {/* Body Type */}
          <div className="control-group">
            <label>👤 Body</label>
            <select 
              value={avatar.bodyType} 
              onChange={(e) => updateAvatar('bodyType', e.target.value)}
              className="control-select"
            >
              {bodyTypes.map(type => (
                <option key={type} value={type}>
                  {type.replace('_', ' ').toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          {/* Eye Type */}
          <div className="control-group">
            <label>👁️ Eyes</label>
            <select 
              value={avatar.eyeType} 
              onChange={(e) => updateAvatar('eyeType', e.target.value)}
              className="control-select"
            >
              {eyeTypes.map(type => (
                <option key={type} value={type}>
                  {type.replace('_', ' ').toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          {/* Mouth Type */}
          <div className="control-group">
            <label>👄 Mouth</label>
            <select 
              value={avatar.mouthType} 
              onChange={(e) => updateAvatar('mouthType', e.target.value)}
              className="control-select"
            >
              {mouthTypes.map(type => (
                <option key={type} value={type}>
                  {type.replace('_', ' ').toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          {/* Accessory */}
          <div className="control-group">
            <label>🎩 Accessory</label>
            <select 
              value={avatar.accessory} 
              onChange={(e) => updateAvatar('accessory', e.target.value)}
              className="control-select"
            >
              {accessories.map(type => (
                <option key={type} value={type}>
                  {type.toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          {/* Primary Color */}
          <div className="control-group">
            <label>🎨 Primary Color</label>
            <input 
              type="color" 
              value={avatar.primaryColor} 
              onChange={(e) => updateAvatar('primaryColor', e.target.value)}
              className="control-color"
            />
          </div>

          {/* Accent Color */}
          <div className="control-group">
            <label>✨ Accent Color</label>
            <input 
              type="color" 
              value={avatar.accentColor} 
              onChange={(e) => updateAvatar('accentColor', e.target.value)}
              className="control-color"
            />
          </div>

          {/* Buttons */}
          <div className="button-group">
            <button 
              onClick={handleSave}
              disabled={saving}
              className="btn btn-primary"
            >
              {saving ? '💾 Saving...' : '💾 Save Avatar'}
            </button>
            <button 
              onClick={handleRandomize}
              className="btn btn-secondary"
            >
              🎲 Randomize
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

AvatarCustomizer.propTypes = {
  onSave: PropTypes.func,
};

export default AvatarCustomizer;
