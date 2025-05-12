// api/getStateInstance.ts

import axios from 'axios';
import { config } from '../config/env';

// Функция для получения состояния инстанса
export const getStateInstance = async () => {
  const url = `${config.apiUrl}/waInstance${config.idInstance}/getStateInstance/${config.apiTokenInstance}`;
  
  try {
    const response = await axios.get(url);
    return response;  // Возвращаем ответ от API
  } catch (error) {
    console.error('Error getting state:', error);
    throw error;  // Бросаем ошибку, если что-то пошло не так
  }
};
