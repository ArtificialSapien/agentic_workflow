import React from "react";

interface ContentPromptInputProps {
  prompt: string;
  onPromptChange: (val: string) => void;
  platform: string;
  onPlatformChange: (val: string) => void;
  tone: string;
  onToneChange: (val: string) => void;
  isBasicMode: boolean;
}

const ContentPromptInput: React.FC<ContentPromptInputProps> = ({
  prompt,
  onPromptChange,
  platform,
  onPlatformChange,
  tone,
  onToneChange,
  isBasicMode,
}) => {
  return (
    <div className="max-w-4xl mx-auto bg-white p-6 rounded-4xl shadow-accent-dark space-y-6">
      {/* Prompt Input */}
      <div>
        <label className="block text-sm font-semibold text-primary-700 mb-2">
          Your Prompt
        </label>
        <textarea
          className="w-full border border-gray-300 rounded-lg p-3 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition"
          rows={3}
          value={prompt}
          onChange={(e) => onPromptChange(e.target.value)}
          placeholder="Write your content prompt here..."
        ></textarea>
      </div>

      {/* Advanced Options */}
      {!isBasicMode && (
        <div className="grid grid-cols-2 gap-6">
          {/* Platform Selector */}
          <div>
            <label className="block text-sm font-semibold text-primary-700 mb-2">
              Platform
            </label>
            <select
              className="w-full border border-gray-300 rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition"
              value={platform}
              onChange={(e) => onPlatformChange(e.target.value)}
            >
              <option value="">Select a platform</option>
              <option>LinkedIn</option>
              <option>Twitter</option>
              <option>Instagram</option>
              <option>Facebook</option>
              <option>TikTok</option>
            </select>
          </div>

          {/* Tone Selector */}
          <div>
            <label className="block text-sm font-semibold text-primary-700 mb-2">
              Tone
            </label>
            <select
              className="w-full border border-gray-300 rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition"
              value={tone}
              onChange={(e) => onToneChange(e.target.value)}
            >
              <option value="">Select a tone</option>
              <option>Professional</option>
              <option>Casual</option>
              <option>Humorous</option>
              <option>Educational</option>
              <option>Inspiring</option>
            </select>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContentPromptInput;
