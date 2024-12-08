// src/components/ContentGeneratorSection.tsx

import React, { useState } from 'react';
import ModeSelector from './ModeSelector';
import ContentPromptInput from './ContentPromptInput';
import ContentFormatSelector from './ContentFormatSelector';
import ContentPreview from './ContentPreview';
import { Mode, GeneratedContent } from '@/types/content';
import { useGenerateContent, useRefineContent } from '@/hooks/useContentGeneration';
import useAuthStore from '@/store/useAuthStore';
import Loader from '../ui/Loader';
import ErrorMessage from '../ui/ErrorMessage';

const ALLOW_GUEST = import.meta.env.VITE_ALLOW_GUEST === 'true';

interface ContentGeneratorSectionProps {
  odd: boolean;
}

const ContentGeneratorSection: React.FC<ContentGeneratorSectionProps> = ({ odd }) => {
  // State management
  const [mode, setMode] = useState<Mode>('guided');
  const [prompt, setPrompt] = useState('');
  const [platform, setPlatform] = useState('LinkedIn');
  const [tone, setTone] = useState('Professional');
  const [generateText, setGenerateText] = useState(true);
  const [generateImage, setGenerateImage] = useState(false);
  const [generateVideo, setGenerateVideo] = useState(false);
  const [generateMeme, setGenerateMeme] = useState(false);

  // Auth Store
  const isGuest = useAuthStore((state) => state.isGuest);
  const guestUsed = useAuthStore((state) => state.guestUsed);
  // const setGuest = useAuthStore((state) => state.setGuest);
  const useGuestOnce = useAuthStore((state) => state.useGuestOnce);

  // React Query Mutations
  const { mutate: generate, data: generatedData, status: generateStatus, error: genError } = useGenerateContent();
  const { mutate: refine, data: refinedData, status: refineStatus, error: refError } = useRefineContent();

  const generatedContent: GeneratedContent = {
    text: refinedData?.generated_text ?? generatedData?.generated_text ?? '',
    imageUrl: generatedData?.image_url ?? '',
    videoUrl: generatedData?.video_url ?? '',
    memeUrl: generatedData?.meme?.meme_url ?? '',
  };

  // Check if generation is allowed
  const canGenerate = (): boolean => {
    if (ALLOW_GUEST && !guestUsed) return true;
    return !isGuest;
  };

  // Handle generate content
  const handleGenerate = () => {
    if (!canGenerate()) {
      alert('Guest access is not available or has already been used. Please try again later.');
      return;
    }

    generate(
      {
        prompt,
        generate_text: generateText,
        generate_image: generateImage,
        generate_video: generateVideo,
        generate_meme: generateMeme,
      },
      {
        onSuccess: () => {
          if (ALLOW_GUEST) {
            useGuestOnce(); // Update guest usage
          }
        },
        onError: (error) => {
          console.error('Error generating content:', error);
        },
      }
    );
  };

  // Handle refine content
  const handleRefine = (refinePrompt: string, originalText: string) => {
    if (!refinePrompt.trim()) return;

    refine(
      { prompt: refinePrompt, generated_text: originalText },
      {
        onError: (error) => {
          console.error('Error refining content:', error);
        },
      }
    );
  };

  return (
    <section
      id="content-generator-section"
      className={`bg-gradient-to-b ${odd ? 'from-primary-100 to-white' : 'from-white to-primary-100'} text-center py-20`}
    >
      {(generateStatus === 'pending' || refineStatus === 'pending') && <Loader text="Generating content..." />}

      <div className="max-w-4xl mx-auto p-6 rounded-lg relative">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-2xl font-semibold">Content Generator</h3>
          <ModeSelector mode={mode} onChange={setMode} />
        </div>

        {/* Guest Access Information */}
        {ALLOW_GUEST && !guestUsed && (
          <div className="mb-4 text-blue-500">
            You are in guest mode. You can generate content once without logging in.
          </div>
        )}

        {ALLOW_GUEST && guestUsed && (
          <div className="mb-4 text-orange-500">
            Your guest attempt has already been used. Please try again later or register.
          </div>
        )}

        <div className="max-w-4xl mx-auto p-6 rounded-4xl space-y-8">
          {/* Guest Access Warning */}
          {!ALLOW_GUEST && !isGuest && (
            <div className="mb-4 text-red-500 font-semibold">
              Guest access is disabled. Please register to generate content.
            </div>
          )}

          {/* Content Format Selector */}
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-primary-700">Select Content Type</h2>
            <p className="text-sm text-gray-600">
              Choose the formats you'd like to create, such as text, images, videos, or memes. You can use the "Select All" button to quickly pick all options.
            </p>
            <ContentFormatSelector
              generateText={generateText}
              setGenerateText={setGenerateText}
              generateImage={generateImage}
              setGenerateImage={setGenerateImage}
              generateVideo={generateVideo}
              setGenerateVideo={setGenerateVideo}
              generateMeme={generateMeme}
              setGenerateMeme={setGenerateMeme}
            />
          </div>

          {/* Content Prompt Input */}
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-primary-700">Create Your Prompt</h2>
            <p className="text-sm text-gray-600">
              Provide a prompt for the content you'd like to generate. Specify the platform and tone to customize the output.
            </p>
            <ContentPromptInput
              prompt={prompt}
              onPromptChange={setPrompt}
              platform={platform}
              onPlatformChange={setPlatform}
              tone={tone}
              onToneChange={setTone}
              isBasicMode={mode === 'basic'}
            />
          </div>
        </div>

        <div className="mt-6 flex justify-end space-x-2">
          <button
            onClick={handleGenerate}
            disabled={!canGenerate()}
            className={`px-4 py-2 text-sm rounded ${
              canGenerate()
                ? 'bg-blue-600 text-white hover:bg-blue-700'
                : 'bg-gray-400 text-white cursor-not-allowed'
            }`}
          >
            Generate Content
          </button>
        </div>

        {(genError || refError) && (
          <ErrorMessage message={genError?.message || refError?.message || 'An error occurred'} />
        )}

        {/* Integrate ContentPreview Component */}
        <ContentPreview 
          generatedContent={generatedContent} 
          onRefine={handleRefine} 
          onPublishAll={() => {}} 
          onSchedule={() => {}} 
          onRegenerateAll={() => {}} 
          onDownloadPack={() => {}} 
          onShareAll={() => {}} 
        />
      </div>
    </section>
  );
};

export default ContentGeneratorSection;
