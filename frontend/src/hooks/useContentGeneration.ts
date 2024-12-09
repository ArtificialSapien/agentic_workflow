import { useMutation, UseMutationResult, useQueryClient } from '@tanstack/react-query';
import { generatePost, finetunePost,finetuneMeme } from '@/api/contentService';
import { InitialRequest, FineTuneTextRequest, InitialResponse, FineTuneMemeRequest, Meme } from '@/types/api';

export function useGenerateContent(): UseMutationResult<InitialResponse, Error, InitialRequest> {
  const queryClient = useQueryClient();

  return useMutation<InitialResponse, Error, InitialRequest>({
    mutationFn: generatePost, 
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['generatedContent'] }); 
    },
  });
}

export function useRefineContent(): UseMutationResult<{ generated_text: string }, Error, FineTuneTextRequest> {
  const queryClient = useQueryClient();

  return useMutation<{ generated_text: string }, Error, FineTuneTextRequest>({
    mutationFn: finetunePost, 
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['generatedContent'] }); 
    },
  });
}

export function useRefineMeme(): UseMutationResult<Meme, Error, FineTuneMemeRequest> {
  const queryClient = useQueryClient();

  return useMutation<Meme, Error, FineTuneMemeRequest>({
    mutationFn: finetuneMeme,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['generatedContent'] });
    },
  });
}



