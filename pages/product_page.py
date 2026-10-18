import re
from playwright.sync_api import Locator
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.core.button import Button
from pages.core.label import Label


class ProductPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.lbl_page_heading = Label(page.get_by_text("Products", exact=True))
        self.lbl_inventory_item_name = Label(self.page.get_by_test_id("inventory-item-name"))
        self.lbl_inventory_item_price = Label(page.get_by_test_id("inventory-item-price"))
        self.lst_inventory_items = Label(page.get_by_test_id("inventory-item"))
        self.btn_add_to_cart = Button(page.get_by_role("button", name="Add to Cart"))
        self.btn_cart = Button(page.get_by_test_id("shopping-cart-link"))
        self.btn_remove_cart = Button(page.get_by_role("button", name="Remove"))

    def get_page_heading(self) -> str:
        """
        Get the heading of the page.

        Returns:
              str: Heading of the page
        """
        return self.lbl_page_heading.get_text()

    def get_inventory_item(self, item_name: str) -> Locator:
        """
        Return the inventory card whose name exactly matches `item_name`.

        Args:
            item_name (str): The name of the item to look for.

        Returns:
            Locator: The locator for the inventory item card.
        """
        _name = self.lbl_inventory_item_name.locator.filter(has_text=re.compile(rf"^{re.escape(item_name)}$"))
        return self.lst_inventory_items.locator.filter(has=_name)

    def get_item_price(self, item_name: str) -> float:
        """
        Get the price of the given item as a number, e.g. 29.99.
        Args:
            item_name (str): The name of the item to look for.

        Returns:
            float: The price of the item.
        """
        _lbl_price = Label(self.get_inventory_item(item_name).locator(self.lbl_inventory_item_price.locator))
        _price_text = _lbl_price.get_label_text()
        return float(_price_text.replace("$", "").strip())

    def get_button_add_to_cart(self, item_name: str) -> Button:
        """
        Get the 'Add to Cart' button for the given item.

        Args:
            item_name (str): The name of the item to look for.

        Returns:
            Button (Locator): The 'Add to Cart' button Locator for the given item.
        """
        return Button(self.get_inventory_item(item_name).locator(self.btn_add_to_cart.locator))

    def is_display_add_to_cart(self, item_name: str) -> bool:
        """
        Return True if the 'Add to Cart' button for the given item is displayed.

        Args:
            item_name (str): The name of the item to look for.

        Returns:
            bool: True if the 'Add to Cart' button is displayed, False otherwise.
        """
        _btn_add_to_cart = self.get_button_add_to_cart(item_name)
        return _btn_add_to_cart.is_displayed()

    def click_add_to_cart(self, item_name: str) -> None:
        """
        Click the 'Add to Cart' button for the given item.

        Args:
            item_name (str): The name of the item to look for.
        """
        _btn_add_to_cart = self.get_button_add_to_cart(item_name)
        _btn_add_to_cart.click()

    def get_cart_value(self) -> int:
        """
        Get the number of items in the cart.

        Returns:
            int: Number of items in the cart.
        """
        _value = self.btn_cart.locator.get_attribute("aria-label")
        if "empty" in _value:
            return 0
        _match = re.search(r"\d+", _value)
        if not _match:
            raise ValueError(f"Unexpected cart aria-label: '{_value}'")
        return int(_match.group())

    def get_button_remove(self, item_name: str) -> Button:
        """
        Return the 'Remove' button for the given item.

        Args:
            item_name (str): The name of the item to look for.

        Returns:
            Button (Locator): The 'Remove' button Locator for the given item.
        """
        return Button(self.get_inventory_item(item_name).locator(self.btn_remove_cart.locator))

    def click_on_cart(self) -> CartPage:
        """
        Click the cart button and return the CartPage.

        Returns:
            CartPage: The CartPage.
        """
        self.btn_cart.click()
        return CartPage(self.page)
