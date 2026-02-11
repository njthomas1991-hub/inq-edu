import React, { useEffect, useRef, useState } from 'react';
import Phaser from 'phaser';
import { fetchKindlewickJson } from '../utils/kindlewickApi';

const GAME_TYPE = 'map';
const LEVEL = 1;

const KindlewickRuntime = ({ onSessionComplete }) => {
  const containerRef = useRef(null);
  const gameRef = useRef(null);
  const sessionIdRef = useRef(null);
  const [status, setStatus] = useState(null);

  useEffect(() => {
    let playtimeTimer = null;
    let playtime = 0;

    const createSession = async () => {
      const session = await fetchKindlewickJson('/kindlewick/sessions/', {
        method: 'POST',
        body: JSON.stringify({
          game_type: GAME_TYPE,
          level: LEVEL,
          session_data: { collected: 0 }
        })
      });
      sessionIdRef.current = session.id;
      return session.id;
    };

    const finalizeSession = async (score, tokens, collected) => {
      if (!sessionIdRef.current) {
        return;
      }
      await fetchKindlewickJson(`/kindlewick/sessions/${sessionIdRef.current}/`, {
        method: 'PUT',
        body: JSON.stringify({
          score,
          tokens_earned: tokens,
          playtime,
          completed: true,
          session_data: { collected }
        })
      });
      setStatus('Session complete. Progress saved.');
      if (onSessionComplete) {
        onSessionComplete();
      }
    };

    const config = {
      type: Phaser.AUTO,
      width: 540,
      height: 320,
      parent: containerRef.current,
      backgroundColor: '#0f172a',
      scene: {
        preload() {
          this.load.image('orb', 'https://assets.codepen.io/1320943/orb.png');
        },
        async create() {
          await createSession();
          setStatus('Collect 6 glow orbs to finish the session.');

          const target = 6;
          let collected = 0;
          let score = 0;

          const label = this.add.text(20, 20, 'Kindlewick Trail', {
            fontFamily: 'Space Grotesk, Trebuchet MS, sans-serif',
            fontSize: '20px',
            color: '#f8fafc'
          });

          const counter = this.add.text(20, 50, 'Collected: 0/6', {
            fontFamily: 'Space Grotesk, Trebuchet MS, sans-serif',
            fontSize: '16px',
            color: '#e2e8f0'
          });

          const info = this.add.text(20, 75, 'Click glowing orbs to collect.', {
            fontFamily: 'Space Grotesk, Trebuchet MS, sans-serif',
            fontSize: '14px',
            color: '#94a3b8'
          });

          const spawnOrb = () => {
            const orb = this.add.image(
              Phaser.Math.Between(60, 480),
              Phaser.Math.Between(110, 280),
              'orb'
            );
            orb.setScale(0.35 + Math.random() * 0.2);
            orb.setInteractive({ useHandCursor: true });
            orb.on('pointerdown', async () => {
              orb.destroy();
              collected += 1;
              score += 120;
              counter.setText(`Collected: ${collected}/${target}`);
              if (collected >= target) {
                info.setText('Great job! Saving your progress...');
                await finalizeSession(score, collected, collected);
              } else {
                spawnOrb();
              }
            });
          };

          spawnOrb();

          playtimeTimer = window.setInterval(() => {
            playtime += 1;
          }, 1000);

          this.events.on('shutdown', () => {
            if (playtimeTimer) {
              window.clearInterval(playtimeTimer);
            }
          });
        }
      }
    };

    const game = new Phaser.Game(config);
    gameRef.current = game;

    return () => {
      if (playtimeTimer) {
        window.clearInterval(playtimeTimer);
      }
      if (gameRef.current) {
        gameRef.current.destroy(true);
        gameRef.current = null;
      }
    };
  }, [onSessionComplete]);

  return (
    <div className="kw-runtime">
      <div className="kw-runtime-header">
        <div>
          <h3>Kindlewick Micro-Quest</h3>
          <p>Play a short session to log real tracking data.</p>
        </div>
        {status && <span className="kw-runtime-status">{status}</span>}
      </div>
      <div className="kw-runtime-canvas" ref={containerRef} />
    </div>
  );
};

export default KindlewickRuntime;
