import { test, expect } from '@playwright/test';

test('Request A Quote Form - Negative Test', async ({ page }) => {
  // Переходим на страницу с формой
  await page.goto('https://qatest.datasub.com/', { timeout: 60000 });

  // Ждем появления формы
  await page.waitForSelector('form');

  // Заполняем поля формы (с ошибкой в email)
  await page.fill('#name', 'Jane Doe'); // Заполняем поле имени
  await page.fill('#email', 'invalidemail'); // Заполняем поле с неправильным email
  await page.selectOption('#service', { value: 'A Service' }); // Выбираем услугу A
  await page.fill('#message', 'Test message.'); // Заполняем сообщение

  // Кликаем по кнопке отправки
  await page.click('button[type="submit"]');

  // Ожидаем появления сообщения об ошибке
  await expect(page.getByText('Invalid email address')).toBeVisible();
});
