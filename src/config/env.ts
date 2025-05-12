// config/env.ts
import dotenv from 'dotenv';
dotenv.config();

if (
  !process.env.API_URL ||
  !process.env.MEDIA_URL ||
  !process.env.ID_INSTANCE ||
  !process.env.API_TOKEN_INSTANCE ||
  !process.env.CHAT_ID
) {
  throw new Error('Missing required environment variables');
}

export const config = {
  apiUrl: process.env.API_URL,
  mediaUrl: process.env.MEDIA_URL,
  idInstance: process.env.ID_INSTANCE,
  apiTokenInstance: process.env.API_TOKEN_INSTANCE,
  chatId: process.env.CHAT_ID,
};
