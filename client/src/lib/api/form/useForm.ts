import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api, { getCSRFToken } from "../api";

export interface Question {
  id: string;
  question: string;
  required: boolean;
  answer_type: string;
  min_len: number;
  max_len: number;
  options: string;
  file_type: string;
}

export interface FormQuestion {
  id: string;
  question: Question;
  form_index: number;
}

export interface Form {
  id: string;
  name: string;
  form_questions: FormQuestion[];
}

export interface FormSubmissionData {
  user_code: string;
  formId: string;
  responses: Record<string, any>;
}

export interface FormSubmissionResponse {
  message: string;
  response_id: string;
}

const fetchForm = async (formId: string): Promise<Form> => {
  const response = await api.get(`/forms/${formId}/`);
  return response.data;
};

const submitFormResponse = async (
  data: FormData | FormSubmissionData,
): Promise<FormSubmissionResponse> => {
  const response = await api.post("/forms/submit", data, {
    headers: {
      "Content-Type":
        data instanceof FormData ? "multipart/form-data" : "application/json",
    },
  });
  return response.data;
};

export const useForm = (formId: string) => {
  return useQuery({
    queryKey: ["form", formId],
    queryFn: () => fetchForm(formId),
    enabled: !!formId,
  });
};

export const useSubmitFormResponse = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: submitFormResponse,
    onSuccess: (data, variables) => {
      // Invalidate and refetch form data if needed
      queryClient.invalidateQueries({ queryKey: ["form", variables.formId] });
    },
  });
};

// Hook to initialize CSRF token
export const useInitializeCSRF = () => {
  return useQuery({
    queryKey: ["csrf-token"],
    queryFn: getCSRFToken,
    staleTime: 1000 * 60 * 60, // 1 hour
    gcTime: 1000 * 60 * 60 * 24, // 24 hours
  });
};

// AI Form Fill Types
export interface AIFillRequest {
  formId: string;
  userInput: string;
}

export interface AIFillResponse {
  success: boolean;
  responses: Record<string, any>;
}

// AI Form Fill API function
const aiFillForm = async (data: AIFillRequest): Promise<AIFillResponse> => {
  const response = await api.post("/forms/ai-fill", data);
  return response.data;
};

// Hook to use AI form fill
export const useAIFillForm = () => {
  return useMutation({
    mutationFn: aiFillForm,
  });
};
