// src/types/api.ts

// Initial Request Interface
export interface InitialRequest {
  prompt: string;
  generate_text?: boolean;
  generate_image?: boolean;
  generate_video?: boolean;
  generate_meme?: boolean;
  // Uncomment if you decide to include these fields
  // user_id?: string;
  // session_id?: string;
}

// Initial Response Interface
export interface InitialResponse {
  generated_text: string;
  image_url: string;
  video_url: string;
  meme: Meme;
}

// Fine-Tune Text Request Interface
export interface FineTuneTextRequest {
  prompt: string;
  generated_text: string;
  // Uncomment if you decide to include these fields
  // user_id?: string;
  // session_id?: string;
}

// Fine-Tune Meme Request Interface
export interface FineTuneMemeRequest {
  prompt: string;
  meme: Meme;
  // Uncomment if you decide to include these fields
  // user_id?: string;
  // session_id?: string;
}

// Fine-Tuned Text Response Interface
export interface FineTunedText {
  generated_text: string;
}

// Fine-Tuned Image Response Interface
export interface FineTunedImage {
  image_url: string;
}

// Fine-Tuned Video Response Interface
export interface FineTunedVideo {
  video_url: string;
}

// Meme Interface
export interface Meme {
  meme_template?: MemeTemplate;
  meme_url?: string;
}

// Meme Template Interface
export interface MemeTemplate {
  id: string;
  name: string;
  url: string;
  width: number;
  height: number;
  box_count: number;
}

// News Article Interfaces (if needed in frontend)
export interface NewsArticle {
  title: string;
  date: string;
  content: string;
  author: string;
  source: string;
  // Uncomment if you decide to include these fields
  // query_api?: string;
  // query_prompt?: string;
}

export interface NewsArticles {
  articles: NewsArticle[];
}

// Meme Captions Interface (if needed)
export interface MemeCaptions {
  captions: string[];
}

// Generation Options Interface
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

// Generated Content Interface
export interface GeneratedContent {
  text?: string;
  imageUrl?: string;
  videoUrl?: string;
  memeUrl?: string;
}
