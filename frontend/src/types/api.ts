// src/types/api.ts

export interface InitialRequest {
    prompt: string;
    generate_text?: boolean;
    generate_image?: boolean;
    generate_video?: boolean;
    generate_meme?: boolean;
  }
  
  export interface InitialResponse {
    generated_text: string;
    image_url: string;
    video_url: string;
    meme_url: string;
  }
  
  export interface FineTuneRequest {
    prompt: string;
    generated_text: string;
  }
  
  export interface FineTunedText {
    generated_text: string;
  }