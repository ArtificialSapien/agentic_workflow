import axios from 'axios';
import { InitialRequest, InitialResponse,Meme, FineTuneTextRequest, FineTunedText,FineTuneMemeRequest, ContentAnalysisRequest, ContentAnalysisResponse } from '../types/api';

//TODO Set baseURL from env variable for flexibility
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

export async function generatePost(requestData: InitialRequest): Promise<InitialResponse> {
  const response = await api.post<InitialResponse>('/post_prompt/generate_post/', requestData);
  return response.data;
}

export async function finetunePost(requestData: FineTuneTextRequest): Promise<FineTunedText> {
  const response = await api.post<FineTunedText>('/fine_tune_text/finetune_post/', requestData);
  return response.data;
}
export async function finetuneMeme(requestData: FineTuneMemeRequest): Promise<Meme> {
  const response = await api.post<Meme>('/fine_tune_meme/finetune_meme/', requestData);
  return response.data;
}

export async function analyseContent(requestData: ContentAnalysisRequest): Promise<ContentAnalysisResponse> {
  const response = await api.post<ContentAnalysisResponse>('/content_analysis/analyse_content/', requestData);
  return response.data;
}
