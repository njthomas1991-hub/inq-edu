import React, { useEffect, useMemo, useState } from 'react';
import { fetchKindlewickJson } from '../utils/kindlewickApi';

const KindlewickTeacherPanel = ({ user }) => {
  const [filters, setFilters] = useState({
    classId: '',
    studentId: '',
    teacherId: ''
  });
  const [progress, setProgress] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(false); // collapsed by default

  const basePath = useMemo(() => {
    if (!user) {
      return null;
    }
    if (user.role === 'school_admin') {
      return '/kindlewick/school-admin';
    }
    if (user.role === 'teacher') {
      return '/kindlewick/teacher';
    }
    return null;
  }, [user]);

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const buildQuery = () => {
    const params = new URLSearchParams();
    if (filters.classId) {
      params.set('class_id', filters.classId);
    }
    if (filters.studentId) {
      params.set('student_id', filters.studentId);
    }
    if (filters.teacherId && user?.role === 'school_admin') {
      params.set('teacher_id', filters.teacherId);
    }
    params.set('limit', '150');
    const query = params.toString();
    return query ? `?${query}` : '';
  };

  const loadTracking = async () => {
    if (!basePath) {
      return;
    }
    setLoading(true);
    setStatus(null);
    const query = buildQuery();
    try {
      const [progressData, sessionData] = await Promise.all([
        fetchKindlewickJson(`${basePath}/progress/${query}`),
        fetchKindlewickJson(`${basePath}/sessions/${query}`)
      ]);
      setProgress(progressData);
      setSessions(sessionData);
      setStatus({ type: 'success', message: 'Tracking data loaded.' });
    } catch (error) {
      setStatus({ type: 'error', message: `Unable to load tracking data: ${error.message}` });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (basePath && expanded) {
      loadTracking();
    }
  }, [basePath, expanded]);

  if (!basePath) {
    return null;
  }

  return (
    <section className="kw-react-card kw-teacher-panel">
      <header className="kw-teacher-header">
        <div>
          <h3>Kindlewick Tracking (Teacher/Admin)</h3>
          <p>Review progress and session data across your assigned students.</p>
        </div>
        <button
          type="button"
          onClick={() => setExpanded((prev) => !prev)}
          aria-expanded={expanded}
          aria-controls="kw-teacher-panel-content"
        >
          {expanded ? 'Hide Panel' : 'Show Panel'}
        </button>
      </header>
      {expanded && (
        <div id="kw-teacher-panel-content">
          <div className="kw-teacher-filters">
            <label>
              Class ID
              <input
                type="text"
                name="classId"
                value={filters.classId}
                onChange={handleFilterChange}
                placeholder="Optional"
              />
            </label>
            <label>
              Student ID
              <input
                type="text"
                name="studentId"
                value={filters.studentId}
                onChange={handleFilterChange}
                placeholder="Optional"
              />
            </label>
            {user?.role === 'school_admin' && (
              <label>
                Teacher ID
                <input
                  type="text"
                  name="teacherId"
                  value={filters.teacherId}
                  onChange={handleFilterChange}
                  placeholder="Optional"
                />
              </label>
            )}
          </div>

          {status && (
            <div className={`kw-react-alert ${status.type}`}>{status.message}</div>
          )}

          <div className="kw-teacher-grid">
            <div>
              <h4>Progress Records</h4>
              {progress.length ? (
                <div className="kw-react-list">
                  {progress.map((item) => (
                    <div key={item.id} className="kw-react-item">
                      <strong>{item.user_detail?.first_name || item.user_detail?.username}</strong>
                      <span>{item.game_type_display} • Level {item.current_level}</span>
                      <span>Score {item.score} • Tokens {item.tokens_earned}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="kw-react-muted">No progress records found.</p>
              )}
            </div>
            <div>
              <h4>Session Records</h4>
              {sessions.length ? (
                <div className="kw-react-list">
                  {sessions.map((item) => (
                    <div key={item.id} className="kw-react-item">
                      <strong>{item.user_detail?.first_name || item.user_detail?.username}</strong>
                      <span>{item.game_type_display} • Level {item.level}</span>
                      <span>Score {item.score} • {item.playtime}s</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="kw-react-muted">No sessions recorded.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default KindlewickTeacherPanel;
