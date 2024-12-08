import React from 'react';
import { Mode } from '@/types/content';

interface ModeSelectorProps {
  mode: Mode;
  onChange: (mode: Mode) => void;
}

const ModeSelector: React.FC<ModeSelectorProps> = ({ mode, onChange }) => {
  return (
    <div className="flex space-x-2 bg-gray-100 rounded p-1">
      <button
        className={`px-4 py-2 text-sm rounded-md ${mode === 'basic' ? 'bg-white shadow' : ''}`}
        onClick={() => onChange('basic')}
      >
        Basic Mode
      </button>
      <button
        className={`px-4 py-2 text-sm rounded-md ${mode === 'guided' ? 'bg-white shadow' : ''}`}
        onClick={() => onChange('guided')}
      >
        Guided Mode
      </button>
      <button
        className={`px-4 py-2 text-sm rounded-md ${mode === 'expert' ? 'bg-white shadow' : ''}`}
        onClick={() => onChange('expert')}
      >
        Expert Mode
      </button>
    </div>
  );
};

export default ModeSelector;