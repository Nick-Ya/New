const { test, expect } = require('@playwright/test');
const { LoginPage } = require('../pages/LoginPage');           // <-- Этого не хватает!
const { InventoryPage } = require('../pages/InventoryPage');
const { CartPage } = require('../pages/CartPage');

test('Добавление и удаление товара из корзины', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const inventoryPage = new InventoryPage(page);
  const cartPage = new CartPage(page);

  await loginPage.goto();
  await loginPage.login('standard_user', 'secret_sauce');
  await expect(page).toHaveURL(/inventory/);

  await inventoryPage.addItemToCart();
  await inventoryPage.goToCart();
  await cartPage.removeItem();
  await expect(page.locator('.cart_item')).toHaveCount(0);
});