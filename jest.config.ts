// jest.config.ts

export default {
  preset: 'ts-jest',  // Используем ts-jest для работы с TypeScript
  testEnvironment: 'node',  // Окружение для тестов
  testMatch: ['**/tests/**/*.test.ts'],  // Местоположение тестов
  verbose: true,  // Подробный вывод
  maxWorkers: 1,  // Один поток, отключает многопоточность
};
