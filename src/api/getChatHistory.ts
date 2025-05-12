// api/getChatHistory.ts
import axios from 'axios';
import { config } from '../config/env';

export const getChatHistory = async (chatId = config.chatId) => {
  const url = `${config.apiUrl}/waInstance${config.idInstance}/getChatHistory/${config.apiTokenInstance}`;
  const body = {
    chatId,
    count: 10,
  };

  try {
    const response = await axios.post(url, body);
    return response;
  } catch (error) {
    console.error('Error getting chat history:', error);
    throw error;
  }
};
