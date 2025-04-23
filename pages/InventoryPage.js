class InventoryPage {
  constructor(page) {
    this.page = page;
    this.itemAddToCart = page.locator('button[data-test="add-to-cart-sauce-labs-backpack"]');
    this.cartLink = page.locator('.shopping_cart_link');
  }

  async addItemToCart() {
    await this.itemAddToCart.click();
  }

  async goToCart() {
    await this.cartLink.click();
  }
}

module.exports = { InventoryPage };