
import React from 'react';
import { useTheme } from '../hooks/useTheme';

const CloudAnimation: React.FC = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(5)].map((_, i) => (
        <div
          key={`cloud-${i}`}
          className="cloud absolute text-sky-accent/30 animate-float"
          style={{
            fontSize: `${6 + Math.random() * 6}rem`,
            top: `${Math.random() * 70}%`, // Keep clouds in upper part
            left: `${Math.random() * 100 - 20}%`, // Start some off-screen
            animationDuration: `${20 + Math.random() * 20}s`,
            animationDelay: `${Math.random() * 5}s`,
            transform: `scale(${0.5 + Math.random() * 0.5})`,
          }}
        >
          ☁️
        </div>
      ))}
    </div>
  );
};

const ParticleAnimation: React.FC = () => {
  const { theme } = useTheme();
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(50)].map((_, i) => (
        <div
          key={`particle-${i}`}
          className="particle absolute rounded-full animate-pulseNeon"
          style={{
            width: `${1 + Math.random() * 3}px`,
            height: `${1 + Math.random() * 3}px`,
            backgroundColor: theme.accent, // Use theme accent color
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            animationDuration: `${2 + Math.random() * 3}s`,
            animationDelay: `${Math.random() * 2}s`,
            boxShadow: `0 0 8px ${theme.accent}, 0 0 12px ${theme.accent}`,
            opacity: Math.random() * 0.5 + 0.3,
          }}
        />
      ))}
    </div>
  );
};

const StarfieldAnimation: React.FC = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(100)].map((_, i) => (
        <div
          key={`star-${i}`}
          className="star absolute bg-white rounded-full animate-twinkle"
          style={{
            width: `${1 + Math.random() * 1.5}px`,
            height: `${1 + Math.random() * 1.5}px`,
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            animationDuration: `${3 + Math.random() * 7}s`,
            animationDelay: `${Math.random() * 5}s`,
            opacity: Math.random() * 0.7 + 0.1,
          }}
        />
      ))}
    </div>
  );
};

const AnimatedBackground: React.FC = () => {
  const { theme } = useTheme();

  return (
    <div className={`fixed inset-0 -z-10 transition-all duration-500 ${theme.background}`}>
      {theme.animations.clouds && <CloudAnimation />}
      {theme.animations.particles && <ParticleAnimation />}
      {theme.animations.stars && <StarfieldAnimation />}
    </div>
  );
};

export default AnimatedBackground;