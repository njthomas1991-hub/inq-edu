import React, { useEffect, useState } from 'react';
import '../css/Kindlewick.css';
import KindlewickRuntime from './KindlewickRuntime';
import KindlewickTeacherPanel from './KindlewickTeacherPanel';
import { fetchKindlewickJson } from '../utils/kindlewickApi';

const GAME_TYPES = [
  { value: 'map', label: 'Map Exploration' },
  { value: 'wizards_castle', label: 'Wizards Castle' },
  { value: 'prefixes_potions', label: 'Prefixes and Potions' },
  { value: 'grid_coordinator', label: 'Grid Coordinator' }
];

const KindlewickApp = () => {
  const [user, setUser] = useState(null);
  const [progress, setProgress] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [progressForm, setProgressForm] = useState({
    game_type: 'map',
    current_level: 1,
    score: 0,
    tokens_earned: 0,
    total_playtime: 0,
    completed: false
  });
  const [sessionForm, setSessionForm] = useState({
    game_type: 'map',
    level: 1,
    playtime: 0,
    session_data: ''
  });

  const showStatus = (message, type = 'success') => {
    setStatus({ message, type });
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const [userData, progressData, sessionData] = await Promise.all([
        fetchKindlewickJson('/user/current/'),
        fetchKindlewickJson('/kindlewick/progress/'),
        fetchKindlewickJson('/kindlewick/sessions/')
      ]);
      setUser(userData);
      setProgress(progressData);
      setSessions(sessionData);
      showStatus('Kindlewick data synced.', 'success');
    } catch (error) {
      showStatus(`Unable to load Kindlewick data: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleProgressChange = (event) => {
    const { name, value, type, checked } = event.target;
    setProgressForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSessionChange = (event) => {
    const { name, value } = event.target;
    setSessionForm((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const submitProgress = async (event) => {
    event.preventDefault();
    try {
      await fetchKindlewickJson('/kindlewick/progress/', {
        method: 'POST',
        body: JSON.stringify({
          ...progressForm,
          current_level: Number(progressForm.current_level),
          score: Number(progressForm.score),
          tokens_earned: Number(progressForm.tokens_earned),
          total_playtime: Number(progressForm.total_playtime)
        })
      });
      showStatus('Progress saved.', 'success');
      await loadData();
    } catch (error) {
      showStatus(`Unable to save progress: ${error.message}`, 'error');
    }
  };

  const submitSession = async (event) => {
    event.preventDefault();
    let sessionData = {};

    if (sessionForm.session_data) {
      try {
        sessionData = JSON.parse(sessionForm.session_data);
      } catch (error) {
        showStatus('Session data must be valid JSON.', 'error');
        return;
      }
    }

    try {
      await fetchKindlewickJson('/kindlewick/sessions/', {
        method: 'POST',
        body: JSON.stringify({
          game_type: sessionForm.game_type,
          level: Number(sessionForm.level),
          playtime: Number(sessionForm.playtime),
          session_data: sessionData
        })
      });
      showStatus('Session created.', 'success');
      await loadData();
    } catch (error) {
      showStatus(`Unable to create session: ${error.message}`, 'error');
    }
  };

  const finishSession = async (sessionId) => {
    try {
      await fetchKindlewickJson(`/kindlewick/sessions/${sessionId}/`, {
        method: 'PUT',
        body: JSON.stringify({ completed: true })
      });
      showStatus('Session marked complete.', 'success');
      await loadData();
    } catch (error) {
      showStatus(`Unable to update session: ${error.message}`, 'error');
    }
  };

  const formatGameType = (value) => {
    const match = GAME_TYPES.find((type) => type.value === value);
    return match ? match.label : value;
  };

  return (
    <div className="kw-react">
      <header className="kw-react-hero">
        <div>
          <p className="kw-react-pill">
            {user ? `${user.first_name || user.username} • ${user.role}` : 'Not signed in'}
          </p>
          <h1>Kindlewick Adventure Console</h1>
          <p>Sync progress and session data for the logged-in student profile.</p>
        </div>
        <div className="kw-react-actions">
          <button type="button" className="kw-react-button" onClick={loadData}>
            Refresh
          </button>
          <button
            type="button"
            className="kw-react-button outline"
            onClick={() => {
              if (sessions[0]) {
                finishSession(sessions[0].id);
              }
            }}
          >
            Finish latest session
          </button>
        </div>
      </header>

      {status && (
        <div className={`kw-react-alert ${status.type}`}>{status.message}</div>
      )}

      <section className="kw-react-grid">
        <article className="kw-react-card">
          <h3>Progress Snapshot</h3>
          <form onSubmit={submitProgress} className="kw-react-form">
            <label>
              Game
              <select
                name="game_type"
                value={progressForm.game_type}
                onChange={handleProgressChange}
              >
                {GAME_TYPES.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </label>
            <div className="kw-react-row">
              <label>
                Level
                <input
                  type="number"
                  min="1"
                  name="current_level"
                  value={progressForm.current_level}
                  onChange={handleProgressChange}
                />
              </label>
              <label>
                Score
                <input
                  type="number"
                  min="0"
                  name="score"
                  value={progressForm.score}
                  onChange={handleProgressChange}
                />
              </label>
            </div>
            <div className="kw-react-row">
              <label>
                Tokens
                <input
                  type="number"
                  min="0"
                  name="tokens_earned"
                  value={progressForm.tokens_earned}
                  onChange={handleProgressChange}
                />
              </label>
              <label>
                Playtime (sec)
                <input
                  type="number"
                  min="0"
                  name="total_playtime"
                  value={progressForm.total_playtime}
                  onChange={handleProgressChange}
                />
              </label>
            </div>
            <label className="kw-react-checkbox">
              <input
                type="checkbox"
                name="completed"
                checked={progressForm.completed}
                onChange={handleProgressChange}
              />
              Mark complete
            </label>
            <button type="submit">Save progress</button>
          </form>
        </article>

        <article className="kw-react-card">
          <h3>Start New Session</h3>
          <form onSubmit={submitSession} className="kw-react-form">
            <label>
              Game
              <select
                name="game_type"
                value={sessionForm.game_type}
                onChange={handleSessionChange}
              >
                {GAME_TYPES.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </label>
            <div className="kw-react-row">
              <label>
                Level
                <input
                  type="number"
                  min="1"
                  name="level"
                  value={sessionForm.level}
                  onChange={handleSessionChange}
                />
              </label>
              <label>
                Playtime (sec)
                <input
                  type="number"
                  min="0"
                  name="playtime"
                  value={sessionForm.playtime}
                  onChange={handleSessionChange}
                />
              </label>
            </div>
            <label>
              Session data (JSON)
              <textarea
                name="session_data"
                value={sessionForm.session_data}
                onChange={handleSessionChange}
                placeholder='{"checkpoints": 2, "hints": 1}'
              />
            </label>
            <button type="submit">Create session</button>
          </form>
        </article>
      </section>

      <section className="kw-react-card">
        <h3>Recent Progress</h3>
        {loading ? (
          <p className="kw-react-muted">Loading progress...</p>
        ) : progress.length ? (
          <div className="kw-react-list">
            {progress.map((item) => (
              <div key={item.id} className="kw-react-item">
                <strong>{formatGameType(item.game_type)}</strong>
                <span>Level {item.current_level} • Score {item.score}</span>
                <span>Tokens {item.tokens_earned} • {item.total_playtime}s</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="kw-react-muted">No progress tracked yet.</p>
        )}
      </section>

      <section className="kw-react-card">
        <h3>Latest Sessions</h3>
        {loading ? (
          <p className="kw-react-muted">Loading sessions...</p>
        ) : sessions.length ? (
          <div className="kw-react-list">
            {sessions.map((item) => (
              <div key={item.id} className="kw-react-item">
                <div>
                  <strong>{formatGameType(item.game_type)}</strong> • Level {item.level}
                </div>
                <span>Score {item.score} • Tokens {item.tokens_earned} • {item.playtime}s</span>
                <button type="button" onClick={() => finishSession(item.id)}>
                  {item.completed ? 'View' : 'Finish session'}
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p className="kw-react-muted">No sessions recorded yet.</p>
        )}
      </section>

      <KindlewickTeacherPanel user={user} />

      <KindlewickRuntime onSessionComplete={loadData} />
    </div>
  );
};

export default KindlewickApp;
