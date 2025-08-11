// {
//     "detail": "User code sent to your email"
// }

import { useMutation } from "@tanstack/react-query";
import api from "../api";

export interface UserCodeResponse {
  detail: string;
}

const getUserCode = async (email: string): Promise<UserCodeResponse> => {
  const response = await api.get(`/resend_code/?email=${email}`);
  return response.data;
};

export const useUserCode = () => {
  return useMutation({
    mutationFn: getUserCode,
  });
};
