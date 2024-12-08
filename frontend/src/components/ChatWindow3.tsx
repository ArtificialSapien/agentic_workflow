import React, { useState } from 'react';
import { Send } from 'lucide-react';
import axios from 'axios';

interface ContentGeneratorSectionProps {
  odd: boolean;
}

const ContentGeneratorSection: React.FC<ContentGeneratorSectionProps> = ({ odd }) => {
  const [mode, setMode] = useState<'guided' | 'expert' | 'basic'>('guided');
  const [prompt, setPrompt] = useState('');
  const [tone, setTone] = useState('Professional');
  const [platform, setPlatform] = useState('LinkedIn');
  const [formats, setFormats] = useState<string[]>(['Text Post', 'Image']);
  const [generatedContent, setGeneratedContent] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [refinePrompt, setRefinePrompt] = useState('');
  const [articles, setArticles] = useState<any[]>([]);

  const handleFormatChange = (format: string) => {
    setFormats((prev) =>
      prev.includes(format)
        ? prev.filter((f) => f !== format)
        : [...prev, format]
    );
  };

  const handleGenerate = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/generate-content', {
        prompt,
        tone,
        platform,
        format: formats,
        mode,
      });
      setGeneratedContent(response.data);
      setArticles(response.data.articles || []);
    } catch (error) {
      console.error('Fehler bei der Content-Generierung:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefine = async (type: string) => {
    if (!refinePrompt) return;
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/refine-content', {
        type,
        refinePrompt,
        originalContent: generatedContent[type],
      });
      setGeneratedContent((prev: any) => ({
        ...prev,
        [type]: response.data[type],
      }));
    } catch (error) {
      console.error('Fehler bei der Verfeinerung:', error);
    } finally {
      setLoading(false);
      setRefinePrompt('');
    }
  };

  return (
    <section
      className={`bg-gradient-to-b ${
        odd ? 'from-primary-100 to-white' : 'from-white to-primary-100'
      } text-center py-20`}
    >
      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg shadow-xl">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-center">Generating your content...</p>
          </div>
        </div>
      )}

      {/* Success Message */}
      {!loading && Object.keys(generatedContent).length > 0 && (
        <div className="fixed bottom-4 right-4 bg-green-500 text-white p-3 rounded-lg shadow-lg">
          <p>Content generated successfully!</p>
        </div>
      )}

      <div className="container mx-auto p-6 pt-20">
        {/* Header */}
        <nav className="flex justify-between items-center mb-8">
          <div className="flex items-center space-x-2">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
            <h1 className="text-2xl font-bold text-primary-600">NewsAI</h1>
          </div>
          <div className="space-x-6 hidden md:flex">
            <a href="#features" className="hover:text-blue-200 transition-colors">
              Features
            </a>
            <a href="#templates" className="hover:text-blue-200 transition-colors">
              Templates
            </a>
            <a href="#pricing" className="hover:text-blue-200 transition-colors">
              Pricing
            </a>
            <a href="#about" className="hover:text-blue-200 transition-colors">
              About
            </a>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="text-center py-16 bg-gradient-to-b from-gray-50 to-white rounded-xl shadow-sm mb-12">
          <h2 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-blue-800">
            AI-Powered News Content Studio
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Transform breaking news into engaging social media content with AI-powered insights and creativity.
          </p>
          <div className="flex justify-center space-x-4">
            <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Get Started
            </button>
            <button className="px-6 py-3 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors">
              Watch Demo
            </button>
          </div>
        </section>

        {/* Main Content Area: Two Column Layout */}
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left Column: Content Generator */}
          <div className="lg:w-1/2 bg-white rounded-xl shadow-lg p-6">
            {/* Mode Selector */}
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold">Content Generator</h3>
              <div className="flex items-center space-x-4">
                <div className="flex rounded-lg bg-gray-100 p-1">
                  <button
                    className={`px-4 py-2 text-sm rounded-md ${
                      mode === 'guided' ? 'bg-white shadow' : 'bg-transparent'
                    }`}
                    onClick={() => setMode('guided')}
                  >
                    Guided Mode
                  </button>
                  <button
                    className={`px-4 py-2 text-sm rounded-md ${
                      mode === 'expert' ? 'bg-white shadow' : 'bg-transparent'
                    }`}
                    onClick={() => setMode('expert')}
                  >
                    Expert Mode
                  </button>
                  <button
                    className={`px-4 py-2 text-sm rounded-md ${
                      mode === 'basic' ? 'bg-white shadow' : 'bg-transparent'
                    }`}
                    onClick={() => setMode('basic')}
                  >
                    Basic Mode
                  </button>
                </div>
                <select className="text-sm border rounded p-1">
                  <option>GPT-4</option>
                  <option>Claude</option>
                  <option>Gemini</option>
                </select>
              </div>
            </div>

            {/* Quick Start Templates */}
            {mode !== 'basic' && (
              <div className="mb-6">
                <h4 className="text-sm font-medium text-gray-700 mb-3">Quick Start Templates</h4>
                <div className="grid grid-cols-2 gap-3">
                  <button className="p-4 border rounded-lg hover:bg-blue-50 text-left">
                    <div className="font-medium mb-1">🔥 Trending News</div>
                    <div className="text-sm text-gray-600">Share breaking industry news</div>
                  </button>
                  <button className="p-4 border rounded-lg hover:bg-blue-50 text-left">
                    <div className="font-medium mb-1">💡 Thought Leadership</div>
                    <div className="text-sm text-gray-600">Share insights & expertise</div>
                  </button>
                  <button className="p-4 border rounded-lg hover:bg-blue-50 text-left">
                    <div className="font-medium mb-1">📊 Data Story</div>
                    <div className="text-sm text-gray-600">Turn stats into narratives</div>
                  </button>
                  <button className="p-4 border rounded-lg hover:bg-blue-50 text-left">
                    <div className="font-medium mb-1">🎯 Product Update</div>
                    <div className="text-sm text-gray-600">Announce features & updates</div>
                  </button>
                </div>
              </div>
            )}

            {/* Input Section */}
            <div className="space-y-6">
              {/* Basic Mode */}
              {mode === 'basic' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Your Prompt</label>
                    <textarea
                      className="block w-full rounded-lg border-gray-300 shadow-sm p-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      rows={3}
                      placeholder="Enter your prompt..."
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                    ></textarea>
                  </div>
                  <button
                    onClick={handleGenerate}
                    className="w-full bg-blue-600 text-white rounded-lg py-3 hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2"
                  >
                    <Send className="w-5 h-5" />
                    <span>Generate</span>
                  </button>
                </>
              )}

              {/* Guided & Expert Mode */}
              {mode !== 'basic' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Your Prompt</label>
                    <textarea
                      className="block w-full rounded-lg border-gray-300 shadow-sm p-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      rows={3}
                      placeholder="Create a LinkedIn post about AI trends today..."
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                    ></textarea>
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Platform</label>
                      <select
                        className="block w-full rounded-lg border-gray-300 shadow-sm"
                        value={platform}
                        onChange={(e) => setPlatform(e.target.value)}
                      >
                        <option>LinkedIn</option>
                        <option>Twitter</option>
                        <option>Instagram</option>
                        <option>Facebook</option>
                        <option>TikTok</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Tone</label>
                      <select
                        className="block w-full rounded-lg border-gray-300 shadow-sm"
                        value={tone}
                        onChange={(e) => setTone(e.target.value)}
                      >
                        <option>Professional</option>
                        <option>Casual</option>
                        <option>Humorous</option>
                        <option>Educational</option>
                        <option>Inspirational</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Content Formats</label>
                      <div className="grid grid-cols-2 gap-2">
                        <label className="flex items-center p-2 border rounded-lg hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            className="rounded text-blue-600"
                            checked={formats.includes('Text Post')}
                            onChange={() => handleFormatChange('Text Post')}
                          />
                          <span className="ml-2 text-sm">Text Post</span>
                        </label>
                        <label className="flex items-center p-2 border rounded-lg hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            className="rounded text-blue-600"
                            checked={formats.includes('Image')}
                            onChange={() => handleFormatChange('Image')}
                          />
                          <span className="ml-2 text-sm">Image</span>
                        </label>
                        <label className="flex items-center p-2 border rounded-lg hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            className="rounded text-blue-600"
                            checked={formats.includes('Video')}
                            onChange={() => handleFormatChange('Video')}
                          />
                          <span className="ml-2 text-sm">Video</span>
                        </label>
                        <label className="flex items-center p-2 border rounded-lg hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            className="rounded text-blue-600"
                            checked={formats.includes('Meme')}
                            onChange={() => handleFormatChange('Meme')}
                          />
                          <span className="ml-2 text-sm">Meme</span>
                        </label>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={handleGenerate}
                    className="w-full bg-blue-600 text-white rounded-lg py-3 hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2"
                  >
                    <span>Generate Content</span>
                  </button>
                </>
              )}

              {/* Action Buttons */}
              {mode !== 'basic' && (
                <div className="mt-6 flex justify-between">
                  <button className="px-4 py-2 text-sm border rounded-lg hover:bg-gray-50">
                    Save as Template
                  </button>
                  <div className="space-x-2">
                    <button className="px-4 py-2 text-sm border rounded-lg hover:bg-gray-50">
                      Preview
                    </button>
                    <button className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                      Generate Content
                    </button>
                  </div>
                </div>
              )}

              {/* Pro Features Teaser */}
              <div className="mt-6 bg-gradient-to-r from-purple-500 to-blue-500 text-white p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium mb-1">Unlock Pro Features</h4>
                    <p className="text-sm opacity-90">
                      Access advanced customization, AI training, and more
                    </p>
                  </div>
                  <button className="px-4 py-2 bg-white text-blue-600 rounded-lg text-sm font-medium">
                    Upgrade
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Dynamic Content Selection & Preview */}
          <div className="lg:w-1/2 space-y-6">
            {/* Dynamic Content Selection Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4">Dynamic Content Selection</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                {/* Format selection (checkboxes) */}
                {/* ... */}
              </div>

              {/* Quick Actions */}
              <div className="flex justify-end space-x-3 mb-6">
                <button className="px-4 py-2 text-sm border rounded-lg hover:bg-gray-50">
                  Select All
                </button>
                <button
                  className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  onClick={handleGenerate}
                >
                  Generate Selected
                </button>
              </div>
            </div>

            {/* Post Assembly Preview Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-semibold">Content Preview</h3>
                <div className="flex space-x-2">
                  <button className="px-3 py-1 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Publish All
                  </button>
                  <button className="px-3 py-1 text-sm border rounded-lg hover:bg-gray-50">
                    Schedule
                  </button>
                </div>
              </div>

              {/* Tab Navigation */}
              <div className="border-b border-gray-200 mb-6">
                <nav className="flex space-x-4" aria-label="Tabs">
                  <button className="px-4 py-2 text-sm font-medium text-blue-600 border-b-2 border-blue-600">
                    All Formats
                  </button>
                  <button className="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700">
                    Text Post
                  </button>
                  <button className="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700">
                    Image
                  </button>
                  <button className="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700">
                    Video
                  </button>
                  <button className="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700">
                    Meme
                  </button>
                </nav>
              </div>

              {/* Preview Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Text Post Preview */}
                {generatedContent.textPost && (
                  <div className="border rounded-lg p-4">
                    {/* ... */}
                  </div>
                )}

                {/* Image Preview */}
                {generatedContent.image && (
                  <div className="border rounded-lg p-4">
                    {/* ... */}
                  </div>
                )}

                {/* Video Preview */}
                {generatedContent.video && (
                  <div className="border rounded-lg p-4">
                    {/* ... */}
                  </div>
                )}

                {/* Meme Preview */}
                {generatedContent.meme && (
                  <div className="border rounded-lg p-4">
                    {/* ... */}
                  </div>
                )}
              </div>

              {/* Preview Actions */}
              <div className="mt-6 border-t pt-6">
                <div className="flex justify-between">
                  <div className="space-x-2">
                    <button className="px-4 py-2 text-sm border rounded-lg hover:bg-gray-50">
                      Regenerate All
                    </button>
                    <button className="px-4 py-2 text-sm border rounded-lg hover:bg-gray-50">
                      Download Pack
                    </button>
                  </div>
                  <button className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Share All
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div> 
      </div>
    </section>
  );
};

export default ContentGeneratorSection;