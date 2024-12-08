import { useMutation, UseMutationResult, useQueryClient } from '@tanstack/react-query';
import { generatePost, finetunePost } from '@/api/contentService';
import { InitialRequest, FineTuneRequest, InitialResponse } from '@/types/api';

export function useGenerateContent(): UseMutationResult<InitialResponse, Error, InitialRequest> {
  const queryClient = useQueryClient();

  return useMutation<InitialResponse, Error, InitialRequest>({
    mutationFn: generatePost, 
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['generatedContent'] }); 
    },
  });
}

export function useRefineContent(): UseMutationResult<{ generated_text: string }, Error, FineTuneRequest> {
  const queryClient = useQueryClient();

  return useMutation<{ generated_text: string }, Error, FineTuneRequest>({
    mutationFn: finetunePost, 
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['generatedContent'] }); 
    },
  });
}