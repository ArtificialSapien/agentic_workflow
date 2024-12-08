import axios from 'axios';
import { InitialRequest, InitialResponse, FineTuneTextRequest, FineTunedText } from '../types/api';

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