// LessonCard component
import React from 'react';

export default function LessonCard({ title, description }) {
  return (
    <div className="lesson-card">
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
}
