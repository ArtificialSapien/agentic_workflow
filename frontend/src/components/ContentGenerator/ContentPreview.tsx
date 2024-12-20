// src/components/ContentPreview.tsx

import React, { useState } from 'react';
import {
  FileText,
  Image as ImageIcon,
  Video as VideoIcon,
  Smile,
  Edit3,
  Download,
} from 'lucide-react';
import { GeneratedContent } from '@/types/content'; // Adjust the path based on your project structure
import MarkdownRenderer from '@/components/ui/MarkdownRenderer';

interface ContentPreviewProps {
  generatedContent: GeneratedContent | null;
  onRefine: (refinePrompt: string, originalContent: string) => void;
  onRefineMeme: (refinePrompt: string) => void;
  onPublishAll: () => void;
  onSchedule: () => void;
  onRegenerateAll: () => void;
  onDownloadPack: () => void;
  onShareAll: () => void;
}

const dummyGeneratedContent: GeneratedContent = {
  text: "🚀 Sample Text Post: AI is transforming the way we create content! Here's how:\n\n📈 Increased productivity by 300%\n💡 Enhanced creative output by 85%\n🎯 Boosted audience engagement by 90%\n\nWhat are your thoughts on AI-driven content creation?\n\n#AI #ContentCreation #Innovation",
  //   text: `# 🚀 This Week in Tech: Key Highlights

  // As we dive into the latest in technology and innovation, here are some noteworthy developments you won't want to miss:

  // - **🚗 AI and Safety Concerns**: Researchers have demonstrated that large language model (LLM)-powered robots can be hacked to act in dangerous ways, such as self-driving cars ignoring stop signs. This raises serious questions about safety protocols in AI development[^1].

  // - **📝 New Tools for Collaboration**: OpenAI has introduced ChatGPT Canvas, an AI-powered tool akin to Google Docs, allowing users to write and edit collaboratively. This is available for subscribers at $20/month, promising to enhance productivity[^2].

  // - **🍏 Apple's Strategic Moves**: Apple insists it’s right on time for the generative AI wave, opting for a product-level integration of AI rather than a standalone offering. This approach aligns with their long-term vision[^3].

  // - **🛡️ OpenAI in Defense**: OpenAI has partnered with defense startup Anduril, leveraging AI models to bolster air defense systems. This partnership follows a trend among tech giants establishing ties with the defense industry[^4].

  // - **💸 Crypto Lender Fallout**: Alex Mashinsky, the former CEO of Celsius, has pleaded guilty to fraud, admitting to misleading customers about the use of their funds. This incident highlights ongoing issues within the crypto space[^5].

  // - **🎙️ In-Depth with Sam Altman**: The latest episode of *Uncanny Valley* features a deep dive into Sam Altman’s journey, the CEO of OpenAI, exploring his influential role in the AI landscape[^6].

  // - **💰 OpenAI's New Subscription Model**: OpenAI has launched ChatGPT Pro, offering an enhanced experience for $200/month. This tier is expected to include exclusive AI model access and additional features[^7].

  // - **🤖 AI and Social Equity**: The rise of social-emotional AI raises concerns about equitable access to services traditionally provided by humans, posing challenges for less advantaged communities[^8].

  // - **🏛️ New AI & Crypto Czar**: David Sacks has been appointed by president-elect Trump to lead AI and crypto policy, a move welcomed by industry leaders as critical for American competitiveness[^9].

  // - **🌍 Canva Embraces AI**: CEO Melanie Perkins sees generative AI not as a threat but as an opportunity to enhance the visual creation process, with Canva continuing to democratize design[^10].

  // Stay informed and engaged with these updates that shape our digital landscape!

  // ---

  // ### Sources:
  // [^1]: [Wired - Researchers hacked several robots infused with large language models](https://www.wired.com/story/researchers-llm-ai-robot-violence/)  
  // [^2]: [Wired - How to use ChatGPT Canvas](https://www.wired.com/story/how-to-use-chatgpt-canvas-productivity/)  
  // [^3]: [Wired - The inside story of Apple Intelligence](https://www.wired.com/story/plaintext-the-inside-story-of-apple-intelligence/)  
  // [^4]: [Wired - OpenAI and Anduril defense partnership](https://www.wired.com/story/openai-anduril-defense/)  
  // [^5]: [Wired - Celsius founder pleads guilty](https://www.wired.com/story/celsius-founder-alex-mashinsky-pleads-guilty-to-fraud-crypto-celsius/)  
  // [^6]: [Wired - Uncanny Valley podcast on Sam Altman](https://www.wired.com/story/uncanny-valley-podcast-5-in-sam-altman-we-trust/)  
  // [^7]: [Wired - OpenAI ChatGPT Pro subscription launch](https://www.wired.com/story/openai-chatgpt-pro-subscription/)  
  // [^8]: [Wired - Wealth inequality and access to AI](https://www.wired.com/story/wealth-inequality-personal-service-access-artificial-intelligence/)  
  // [^9]: [Wired - David Sacks appointed as AI & Crypto Czar](https://www.wired.com/story/crypto-industry-hails-david-sacks-czar/)  
  // [^10]: [Wired - Canva CEO's perspective on generative AI](https://www.wired.com/story/canva-ceo-melanie-perkins-interview/)`
  //   ,

  imageUrl: "",//'https://via.placeholder.com/400x300?text=Sample+Image',
  // videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4',
  memeUrl: "", //'https://via.placeholder.com/400x300?text=Sample+Meme',
}

// Helper function to merge objects and replace empty strings with dummy data
const mergeWithDummy = (content: GeneratedContent | null): GeneratedContent => {
  const mergedContent: GeneratedContent = { ...dummyGeneratedContent, ...content };
  // Replace empty string keys with dummy data
  (Object.keys(mergedContent) as (keyof GeneratedContent)[]).forEach((key) => {
    if (mergedContent[key] === '') {
      mergedContent[key] = dummyGeneratedContent[key];
    }
  });
  return mergedContent;
};

// Define the tabs with labels and corresponding keys
const tabs = [
  { label: 'All Formats', key: 'all' },
  { label: 'Text Post', key: 'text' },
  { label: 'Image', key: 'image' },
  { label: 'Meme', key: 'meme' },
  // { label: 'Video', key: 'video' },
];

const ContentPreview: React.FC<ContentPreviewProps> = ({
  generatedContent,
  onRefine,
  onRefineMeme,
  onPublishAll,
  onSchedule,

}) => {
  const [refinePrompt, setRefinePrompt] = useState('');
  const [activeTab, setActiveTab] = useState<'all' | 'text' | 'image' | 'meme'>('all'); //| 'video'

  // Merge generated content with dummy content
  const contentToDisplay = mergeWithDummy(generatedContent);

  // Mapping from tab key to content key
  const tabToContentKey: Record<string, keyof GeneratedContent> = {
    text: 'text',
    image: 'imageUrl',
    video: 'videoUrl',
    meme: 'memeUrl',
  };

  // Handlers for downloading media
  const handleDownload = async (url: string, type: string) => {
    try {
      const response = await fetch(url, { mode: 'cors' });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = `download.${type}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download the file. Please try again.');
    }
  };

  // Function to determine if a content type should be displayed based on the active tab
  const shouldDisplay = (format: keyof GeneratedContent): boolean => {
    if (activeTab === 'all') {
      return !!contentToDisplay[format];
    }
    const contentKey = tabToContentKey[activeTab];
    return contentKey === format;
  };

  return (
    <div className="mt-6 max-w-4xl mx-auto bg-white rounded-3xl shadow-lg p-6">
      {/* Post Assembly Preview Section */}
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-2xl font-semibold text-primary-700">Content Preview</h3>
        <div className="flex space-x-2">
          <button
            onClick={onPublishAll}
            className="flex items-center px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <span className="mr-2">Publish All</span>
            <Download className="w-4 h-4" />
          </button>
          <button
            onClick={onSchedule}
            className="flex items-center px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <span className="mr-2">Schedule</span>
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-4" aria-label="Tabs">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as 'all' | 'text' | 'image' | 'meme')}
              // | 'video'
              className={`px-4 py-2 text-sm font-medium flex items-center space-x-2 ${activeTab === tab.key
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
                } transition-colors`}
            >
              {tab.key === 'text' && <FileText className="w-5 h-5" />}
              {tab.key === 'image' && <ImageIcon className="w-5 h-5" />}
              {tab.key === 'video' && <VideoIcon className="w-5 h-5" />}
              {tab.key === 'meme' && <Smile className="w-5 h-5" />}
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Preview Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Text Post Preview */}
        {shouldDisplay('text') && (
          <div className="border rounded-2xl p-4 shadow-sm hover:shadow-md transition-shadow md:col-span-2">
            <div className="flex justify-between items-center mb-3">
              <div className="flex items-center space-x-2">
                <FileText className="w-5 h-5 text-primary-700" />
                <span className="font-medium text-primary-700"> Text Post</span>
              </div>
              <div className="flex space-x-2">
                {/* Edit Button */}
                <button
                  onClick={() => {

                    document.getElementById('refine_contend')?.scrollIntoView({ behavior: 'smooth' });

                  }}
                  className="p-1 text-blue-600 hover:text-blue-800 rounded-full transition-colors"
                  aria-label="Edit Text Post"
                >
                  <Edit3 className="w-4 h-4" />
                </button>
                {/* Download Button */}
                <button
                  onClick={() =>
                    handleDownload(
                      'data:text/plain;charset=utf-8,' + encodeURIComponent(contentToDisplay.text as string),
                      'txt'
                    )
                  }
                  className="p-1 text-green-600 hover:text-green-800 rounded-full transition-colors"
                  aria-label="Download Text Post"
                >
                  <Download className="w-4 h-4" />
                </button>
              </div>
            </div>
            <div className="rounded-lg text-sm whitespace-pre-wrap">
              <MarkdownRenderer text={contentToDisplay.text as string} />
            </div>
          </div>
        )}

        {/* Image Preview */}
        {shouldDisplay('imageUrl') && (
          <div className="border rounded-2xl p-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex justify-between items-center mb-3">
              <div className="flex items-center space-x-2">
                <ImageIcon className="w-5 h-5 text-primary-700" />
                <span className="font-medium text-primary-700"> Image</span>
              </div>
              <div className="flex space-x-2">
                {/* Edit Button */}
                <button
                  onClick={() => {

                    document.getElementById('refine_contend')?.scrollIntoView({ behavior: 'smooth' });

                  }}
                  className="p-1 text-blue-600 hover:text-blue-800 rounded-full transition-colors"
                  aria-label="Edit Text Post"
                >
                  <Edit3 className="w-4 h-4" />
                </button>
                {/* Download Button */}
                <button
                  onClick={() => handleDownload(contentToDisplay.imageUrl as string, 'jpg')}
                  className="p-1 text-green-600 hover:text-green-800 rounded-full transition-colors"
                  aria-label="Download Image"
                >
                  <Download className="w-4 h-4" />
                </button>
              </div>
            </div>
            <img
              src={contentToDisplay.imageUrl}
              alt="Generated"
              className="rounded-lg w-full h-auto object-cover"
            />
          </div>
        )}

        {/* Video Preview
        {shouldDisplay('videoUrl') && (
          <div className="border rounded-2xl p-4 shadow-sm hover:shadow-md transition-shadow flex flex-col items-center">
            <div className="w-full">
              <div className="flex justify-between items-center mb-3">
                <div className="flex items-center space-x-2">
                  <VideoIcon className="w-5 h-5 text-primary-700" />
                  <span className="font-medium text-primary-700">Video</span>
                </div>
                <div className="flex space-x-2">

                  <button
                    onClick={() => {
                      const newVideoUrl = prompt('Enter new video URL:', contentToDisplay.videoUrl);
                      if (newVideoUrl !== null && newVideoUrl.trim() !== '') {
                        onRefine(newVideoUrl, '');
                      }
                    }}
                    className="p-1 text-blue-600 hover:text-blue-800 rounded-full transition-colors"
                    aria-label="Edit Video"
                  >
                    <Edit3 className="w-4 h-4" />
                  </button>

                  <button
                    onClick={() => handleDownload(contentToDisplay.videoUrl as string, 'mp4')}
                    className="p-1 text-green-600 hover:text-green-800 rounded-full transition-colors"
                    aria-label="Download Video"
                  >
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
            <video
              controls
              src={contentToDisplay.videoUrl}
              className="rounded-lg w-full h-auto"
            />
          </div>
        )} */}

        {/* Meme Preview */}
        {shouldDisplay('memeUrl') && (
          <div className="border rounded-2xl p-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex justify-between items-center mb-3">
              <div className="flex items-center space-x-2">
                <Smile className="w-5 h-5 text-primary-700" />
                <span className="font-medium text-primary-700"> Meme</span>
              </div>
              <div className="flex space-x-2">
                {/* Edit Button */}
                <button
                  onClick={() => {

                    document.getElementById('refine_contend')?.scrollIntoView({ behavior: 'smooth' });

                  }}
                  className="p-1 text-blue-600 hover:text-blue-800 rounded-full transition-colors"
                  aria-label="Edit Text Post"
                >
                  <Edit3 className="w-4 h-4" />
                </button>
                {/* Download Button */}
                <button
                  onClick={() => handleDownload(contentToDisplay.memeUrl as string, 'jpg')}
                  className="p-1 text-green-600 hover:text-green-800 rounded-full transition-colors"
                  aria-label="Download Meme"
                >
                  <Download className="w-4 h-4" />
                </button>
              </div>
            </div>
            <img
              src={contentToDisplay.memeUrl}
              alt="Meme"
              className="rounded-lg w-full h-auto object-cover"
            />
          </div>
        )}
      </div>

      {/* Preview Actions
      <div className="mt-6 border-t pt-6 flex justify-between items-center">
        <div className="space-x-2">
          <button
            onClick={onRegenerateAll}
            className="flex items-center px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <span className="mr-2">Regenerate All</span>
            <Smile className="w-4 h-4" />
          </button>
          <button
            onClick={onDownloadPack}
            className="flex items-center px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <span className="mr-2">Download Pack</span>
            <Download className="w-4 h-4" />
          </button>
        </div>
        <button
          onClick={onShareAll}
          className="flex items-center px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <span className="mr-2">Share All</span>
          <Smile className="w-4 h-4" />
        </button>
      </div> */}

      {/* Refine Input */}
      <div className="mt-6">
        <div className="flex space-x-2" id="refine_contend">
          <input
            type="text"
            placeholder="Refine your content..."
            className="flex-1 border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
            value={refinePrompt}
            onChange={(e) => setRefinePrompt(e.target.value)}
          />
          <button
            onClick={() => {
              if (refinePrompt.trim()) {
                if (activeTab === 'meme') {
                  onRefineMeme(refinePrompt);
                }
                else {
                  onRefine(refinePrompt, contentToDisplay.text as string);
                }
                setRefinePrompt('');
              }
            }}
            className={`flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors ${refinePrompt.trim() ? '' : 'opacity-50 cursor-not-allowed'
              }`}
            disabled={!refinePrompt.trim()}
          >
            <span className="mr-2">Refine</span>
            <Edit3 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ContentPreview;
