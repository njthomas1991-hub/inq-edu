(() => {
  const API_BASE = '/api';
  const GAME_TYPES = [
    { value: 'map', label: 'Map Exploration' },
    { value: 'wizards_castle', label: 'Wizards Castle' },
    { value: 'prefixes_potions', label: 'Prefixes and Potions' },
    { value: 'grid_coordinator', label: 'Grid Coordinator' }
  ];

  const root = document.getElementById('root');
  if (!root) {
    return;
  }

  const app = document.createElement('div');
  app.className = 'kw-app';
  root.appendChild(app);

  app.innerHTML = `
    <div class="kw-shell">
      <section class="kw-hero">
        <div class="kw-hero-content">
          <p class="kw-pill" id="kw-user-pill">Loading user...</p>
          <h1 class="kw-title">Kindlewick Adventure Console</h1>
          <p class="kw-subtitle">Track progress, sync session data, and keep the magic moving for every logged-in student.</p>
          <div class="kw-quick-actions">
            <button class="kw-button primary" id="kw-refresh">Refresh data</button>
            <button class="kw-button secondary" id="kw-mark-complete">Mark current session complete</button>
          </div>
          <div id="kw-status"></div>
        </div>
      </section>

      <section class="kw-card-grid">
        <article class="kw-card">
          <h3>Progress Snapshot</h3>
          <p class="kw-muted">Update your latest progress values. Saved to your account.</p>
          <form class="kw-form" id="kw-progress-form">
            <label>Game</label>
            <select class="kw-select" name="game_type" id="kw-progress-game"></select>
            <div class="kw-row">
              <div>
                <label>Level</label>
                <input class="kw-input" type="number" name="current_level" min="1" value="1" />
              </div>
              <div>
                <label>Score</label>
                <input class="kw-input" type="number" name="score" min="0" value="0" />
              </div>
            </div>
            <div class="kw-row">
              <div>
                <label>Tokens</label>
                <input class="kw-input" type="number" name="tokens_earned" min="0" value="0" />
              </div>
              <div>
                <label>Playtime (sec)</label>
                <input class="kw-input" type="number" name="total_playtime" min="0" value="0" />
              </div>
            </div>
            <label>
              <input type="checkbox" name="completed" /> Mark complete
            </label>
            <button class="kw-button primary" type="submit">Save progress</button>
          </form>
        </article>

        <article class="kw-card">
          <h3>Start New Session</h3>
          <p class="kw-muted">Capture play sessions with optional JSON data.</p>
          <form class="kw-form" id="kw-session-form">
            <label>Game</label>
            <select class="kw-select" name="game_type" id="kw-session-game"></select>
            <div class="kw-row">
              <div>
                <label>Level</label>
                <input class="kw-input" type="number" name="level" min="1" value="1" />
              </div>
              <div>
                <label>Playtime (sec)</label>
                <input class="kw-input" type="number" name="playtime" min="0" value="0" />
              </div>
            </div>
            <label>Session data (JSON)</label>
            <textarea class="kw-textarea" name="session_data" placeholder='{"checkpoints": 3, "hints": 2}'></textarea>
            <button class="kw-button primary" type="submit">Create session</button>
          </form>
        </article>
      </section>

      <section class="kw-card">
        <h3>Recent Progress</h3>
        <div class="kw-list" id="kw-progress-list"></div>
      </section>

      <section class="kw-card">
        <h3>Latest Sessions</h3>
        <div class="kw-list" id="kw-session-list"></div>
      </section>

      <p class="kw-footer">Need a teacher view? Progress records are tied to the logged-in student profile.</p>
    </div>
  `;

  const progressGame = app.querySelector('#kw-progress-game');
  const sessionGame = app.querySelector('#kw-session-game');
  const progressList = app.querySelector('#kw-progress-list');
  const sessionList = app.querySelector('#kw-session-list');
  const statusContainer = app.querySelector('#kw-status');
  const refreshButton = app.querySelector('#kw-refresh');
  const markCompleteButton = app.querySelector('#kw-mark-complete');
  const userPill = app.querySelector('#kw-user-pill');

  const appendOptions = (select) => {
    GAME_TYPES.forEach((type) => {
      const option = document.createElement('option');
      option.value = type.value;
      option.textContent = type.label;
      select.appendChild(option);
    });
  };

  appendOptions(progressGame);
  appendOptions(sessionGame);

  const getCookie = (name) => {
    const cookies = document.cookie.split(';').map((cookie) => cookie.trim());
    const match = cookies.find((cookie) => cookie.startsWith(`${name}=`));
    return match ? decodeURIComponent(match.split('=')[1]) : '';
  };

  const showStatus = (message, type = 'success') => {
    statusContainer.innerHTML = `<div class="kw-alert ${type}">${message}</div>`;
  };

  const fetchJson = async (url, options = {}) => {
    const response = await fetch(url, {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
        ...options.headers
      },
      ...options
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(text || `${response.status} ${response.statusText}`);
    }

    return response.status === 204 ? null : response.json();
  };

  const formatGameType = (value) => {
    const found = GAME_TYPES.find((type) => type.value === value);
    return found ? found.label : value;
  };

  const renderProgress = (items) => {
    if (!items || items.length === 0) {
      progressList.innerHTML = '<p class="kw-muted">No progress tracked yet.</p>';
      return;
    }

    progressList.innerHTML = items
      .map((item) => {
        return `
          <div class="kw-list-item">
            <strong>${formatGameType(item.game_type)}</strong>
            <div class="kw-muted">Level ${item.current_level} • Score ${item.score} • Tokens ${item.tokens_earned}</div>
            <div class="kw-muted">Playtime ${item.total_playtime}s • Completed ${item.completed ? 'yes' : 'no'}</div>
          </div>
        `;
      })
      .join('');
  };

  const renderSessions = (items) => {
    if (!items || items.length === 0) {
      sessionList.innerHTML = '<p class="kw-muted">No sessions recorded yet.</p>';
      return;
    }

    sessionList.innerHTML = items
      .map((item) => {
        return `
          <div class="kw-list-item">
            <strong>${formatGameType(item.game_type)} • Level ${item.level}</strong>
            <div class="kw-muted">Score ${item.score} • Tokens ${item.tokens_earned} • ${item.playtime}s</div>
            <div class="kw-row">
              <span class="kw-muted">${item.completed ? 'Completed' : 'In progress'}</span>
              <button class="kw-button primary" data-session-id="${item.id}">${item.completed ? 'View' : 'Finish session'}</button>
            </div>
          </div>
        `;
      })
      .join('');

    sessionList.querySelectorAll('button[data-session-id]').forEach((button) => {
      button.addEventListener('click', async () => {
        const sessionId = button.getAttribute('data-session-id');
        try {
          await fetchJson(`${API_BASE}/kindlewick/sessions/${sessionId}/`, {
            method: 'PUT',
            body: JSON.stringify({ completed: true })
          });
          showStatus('Session marked complete.', 'success');
          await loadAll();
        } catch (error) {
          showStatus(`Unable to update session: ${error.message}`, 'error');
        }
      });
    });
  };

  const loadAll = async () => {
    try {
      const [user, progress, sessions] = await Promise.all([
        fetchJson(`${API_BASE}/user/current/`),
        fetchJson(`${API_BASE}/kindlewick/progress/`),
        fetchJson(`${API_BASE}/kindlewick/sessions/`)
      ]);
      userPill.textContent = `${user.first_name || user.username} • ${user.role}`;
      renderProgress(progress);
      renderSessions(sessions);
      showStatus('Data synced with your account.', 'success');
    } catch (error) {
      showStatus(`Sign in required or API unavailable: ${error.message}`, 'error');
      userPill.textContent = 'Not signed in';
    }
  };

  app.querySelector('#kw-progress-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const payload = {
      game_type: formData.get('game_type'),
      current_level: Number(formData.get('current_level')),
      score: Number(formData.get('score')),
      tokens_earned: Number(formData.get('tokens_earned')),
      total_playtime: Number(formData.get('total_playtime')),
      completed: formData.get('completed') === 'on'
    };

    try {
      await fetchJson(`${API_BASE}/kindlewick/progress/`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      showStatus('Progress updated.', 'success');
      await loadAll();
    } catch (error) {
      showStatus(`Unable to save progress: ${error.message}`, 'error');
    }
  });

  app.querySelector('#kw-session-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    let sessionData = {};

    const sessionText = formData.get('session_data');
    if (sessionText) {
      try {
        sessionData = JSON.parse(sessionText);
      } catch (error) {
        showStatus('Session data must be valid JSON.', 'error');
        return;
      }
    }

    const payload = {
      game_type: formData.get('game_type'),
      level: Number(formData.get('level')),
      playtime: Number(formData.get('playtime')),
      session_data: sessionData
    };

    try {
      await fetchJson(`${API_BASE}/kindlewick/sessions/`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      showStatus('Session created.', 'success');
      await loadAll();
    } catch (error) {
      showStatus(`Unable to create session: ${error.message}`, 'error');
    }
  });

  refreshButton.addEventListener('click', () => {
    loadAll();
  });

  markCompleteButton.addEventListener('click', async () => {
    const latest = sessionList.querySelector('button[data-session-id]');
    if (!latest) {
      showStatus('No sessions to complete yet.', 'error');
      return;
    }
    latest.click();
  });

  loadAll();
})();
