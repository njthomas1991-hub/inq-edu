// Navbar with dropdown plus a distinct call-to-action button
import React, { useState } from 'react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen((open) => !open);
  const closeMenu = () => setIsOpen(false);

  return (
    <nav className="navbar">
      <button
        className="nav-brand"
        onClick={toggleMenu}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        Inclusive Quest Education ▾
      </button>

      <div className="nav-controls">
        <div className="nav-dropdown" onMouseLeave={closeMenu}>
          {isOpen && (
            <div className="nav-menu">
              <a href="#lessons" onClick={closeMenu}>
                Lessons
              </a>
              <a href="#games" onClick={closeMenu}>
                Games
              </a>
              <a href="#resources" onClick={closeMenu}>
                Resources
              </a>
            </div>
          )}
        </div>

        <button className="btn-primary">Get Started</button>
      </div>
    </nav>
  );
}
