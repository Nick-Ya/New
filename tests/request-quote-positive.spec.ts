import { test, expect } from '@playwright/test';

test('Request A Quote Form - Positive Test', async ({ page }) => {
  // Переходим на страницу с формой
  await page.goto('https://qatest.datasub.com/', { timeout: 60000 });

  // Ждем появления формы (можно уточнить селектор, если нужно)
  await page.waitForSelector('form');

  // Заполняем поля формы
  await page.fill('#name', 'John Doe'); // Заполняем поле имени
  await page.fill('#email', 'john.doe@example.com'); // Заполняем поле email
  await page.selectOption('#service', { value: 'A Service' }); // Выбираем услугу A
  await page.fill('#message', 'I would like to request a quote.'); // Заполняем сообщение

  // Кликаем по кнопке отправки (предположим, что кнопка имеет тип submit)
  await page.click('button[type="submit"]');

  // Ожидаем появления подтверждения успешной отправки формы
  await expect(page.getByText('Thank you for your request')).toBeVisible();
});
