class CartPage {
  constructor(page) {
    this.page = page;
    this.removeButton = page.locator('button[data-test="remove-sauce-labs-backpack"]');
    this.checkoutButton = page.locator('button[data-test="checkout"]');
  }

  async removeItem() {
    await this.removeButton.click();
  }
}

module.exports = { CartPage };