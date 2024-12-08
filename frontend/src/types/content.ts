export type Mode = 'basic' | 'guided' | 'expert';

export interface GenerationOptions {
  mode: Mode;
  prompt: string;
  platform: string;
  tone: string;
  generateText: boolean;
  generateImage: boolean;
  generateVideo: boolean;
  generateMeme: boolean;
}

export interface GeneratedContent {
  text?: string;
  imageUrl?: string;
  videoUrl?: string;
  memeUrl?: string;
}