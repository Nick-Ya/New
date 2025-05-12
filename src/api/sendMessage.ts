// api/sendMessage.ts
import axios from 'axios';
import { config } from '../config/env';

export async function sendMessage(message: string, chatId: string = config.chatId) {
  const url = `${config.apiUrl}/waInstance${config.idInstance}/sendMessage/${config.apiTokenInstance}`;

  const body = {
    chatId,
    message,
  };

  try {
    const response = await axios.post(url, body);
    console.log('Message sent:', response.data);
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
}
