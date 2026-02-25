import React, { useState } from 'react';
import './css/app.css';
import AvatarCustomizer from './components/AvatarCustomizer';
import KindlewickApp from './components/KindlewickApp';

function App() {
  const [view, setView] = useState('kindlewick');

  return (
    <div className="App">
      <nav className="app-nav">
        <button
          type="button"
          className={`app-tab ${view === 'kindlewick' ? 'active' : ''}`}
          onClick={() => setView('kindlewick')}
        >
          Kindlewick Console
        </button>
        <button
          type="button"
          className={`app-tab ${view === 'avatar' ? 'active' : ''}`}
          onClick={() => setView('avatar')}
        >
          Avatar Studio
        </button>
      </nav>
      <div className="app-panel">
        {view === 'kindlewick' ? <KindlewickApp /> : <AvatarCustomizer />}
      </div>
    </div>
  );
}

export default App;
