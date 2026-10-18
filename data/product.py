# data/products.py
PRODUCTS = {
    "backpack": ("Sauce Labs Backpack", 29.99),
    "bike_light": ("Sauce Labs Bike Light", 9.99),
    "bolt_tshirt": ("Sauce Labs Bolt T-Shirt", 15.99),
    "fleece_jacket": ("Sauce Labs Fleece Jacket", 49.99),
    "onesie": ("Sauce Labs Onesie", 7.99),
    "test_shirt": ("Test.allTheThings() T-Shirt (Red)", 15.99),
}

CART_PRODUCT_NAMES = [name for name, _ in list(PRODUCTS.values())[:2]]
