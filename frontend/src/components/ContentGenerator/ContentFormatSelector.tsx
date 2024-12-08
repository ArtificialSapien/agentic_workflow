import React from "react";
import { FileText, Image, Video, Smile } from "lucide-react";

interface ContentFormatSelectorProps {
  generateText: boolean;
  setGenerateText: (val: boolean) => void;
  generateImage: boolean;
  setGenerateImage: (val: boolean) => void;
  generateVideo: boolean;
  setGenerateVideo: (val: boolean) => void;
  generateMeme: boolean;
  setGenerateMeme: (val: boolean) => void;
}

const ContentFormatSelector: React.FC<ContentFormatSelectorProps> = ({
  generateText,
  setGenerateText,
  generateImage,
  setGenerateImage,
  generateVideo,
  setGenerateVideo,
  generateMeme,
  setGenerateMeme,
}) => {
  const allSelected = generateText && generateImage && generateVideo && generateMeme;

  const handleSelectAllToggle = () => {
    const newState = !allSelected;
    setGenerateText(newState);
    setGenerateImage(newState);
    setGenerateVideo(newState);
    setGenerateMeme(newState);
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-4xl shadow-accent-dark p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold text-primary-700">Content Selection</h3>
 <button
          onClick={handleSelectAllToggle}
          className={`px-4 py-2 text-sm rounded-lg transition-colors duration-200 ${
            allSelected
              ? "bg-accent-500 text-white hover:bg-accent-600"
              : "bg-primary-500 text-white hover:bg-primary-600"
          }`}
        >
          {allSelected ? "Deselect All" : "Select All"}
        </button>
      </div>
      <p className="text-sm text-gray-600 mb-4">
        Select the type of content you want to generate. Choose between text posts, images, videos, and memes. Use the "Select All" button to quickly choose all options or deselect them.
      </p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Text Post */}
        <div className="relative group">
          <input
            type="checkbox"
            id="text-format"
            className="peer hidden"
            checked={generateText}
            onChange={() => setGenerateText(!generateText)}
          />
          <label
            htmlFor="text-format"
            className="block p-4 border-2 rounded-xl cursor-pointer peer-checked:border-primary-500 peer-checked:bg-primary-50 transition-colors hover:shadow-md hover:bg-primary-100"
          >
            <div className="flex flex-col items-center text-center">
              <FileText
                className="w-8 h-8 mb-2 text-primary-700 group-hover:scale-110 transition-transform"
              />
              <span className="font-medium text-primary-700">Text</span>
              <span className="text-xs text-gray-500">Social media text</span>
            </div>
          </label>
        </div>

        {/* Image */}
        <div className="relative group">
          <input
            type="checkbox"
            id="image-format"
            className="peer hidden"
            checked={generateImage}
            onChange={() => setGenerateImage(!generateImage)}
          />
          <label
            htmlFor="image-format"
            className="block p-4 border-2 rounded-xl cursor-pointer peer-checked:border-primary-500 peer-checked:bg-primary-50 transition-colors hover:shadow-md hover:bg-primary-100"
          >
            <div className="flex flex-col items-center text-center">
              <Image
                className="w-8 h-8 mb-2 text-primary-700 group-hover:scale-110 transition-transform"
              />
              <span className="font-medium text-primary-700">Image</span>
              <span className="text-xs text-gray-500">AI-generated visual</span>
            </div>
          </label>
        </div>

        {/* Video */}
        <div className="relative group">
          <input
            type="checkbox"
            id="video-format"
            className="peer hidden"
            checked={generateVideo}
            onChange={() => setGenerateVideo(!generateVideo)}
          />
          <label
            htmlFor="video-format"
            className="block p-4 border-2 rounded-xl cursor-pointer peer-checked:border-primary-500 peer-checked:bg-primary-50 transition-colors hover:shadow-md hover:bg-primary-100"
          >
            <div className="flex flex-col items-center text-center">
              <Video
                className="w-8 h-8 mb-2 text-primary-700 group-hover:scale-110 transition-transform"
              />
              <span className="font-medium text-primary-700">Video</span>
              <span className="text-xs text-gray-500">Short video clip</span>
            </div>
          </label>
        </div>

        {/* Meme */}
        <div className="relative group">
          <input
            type="checkbox"
            id="meme-format"
            className="peer hidden"
            checked={generateMeme}
            onChange={() => setGenerateMeme(!generateMeme)}
          />
          <label
            htmlFor="meme-format"
            className="block p-4 border-2 rounded-xl cursor-pointer peer-checked:border-primary-500 peer-checked:bg-primary-50 transition-colors hover:shadow-md hover:bg-primary-100"
          >
            <div className="flex flex-col items-center text-center">
              <Smile
                className="w-8 h-8 mb-2 text-primary-700 group-hover:scale-110 transition-transform"
              />
              <span className="font-medium text-primary-700">Meme</span>
              <span className="text-xs text-gray-500">Viral format</span>
            </div>
          </label>
        </div>
      </div>
    </div>
  );
};

export default ContentFormatSelector;
