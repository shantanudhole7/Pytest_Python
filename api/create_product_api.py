from copy import replace
from api.api_base import ApiBase
from pojo.create_product import CreateProduct


class CreateProductApi(ApiBase):
    _CREATE_PRODUCT_PATH = "api/ecom/product/add-product"

    def __init__(self, request):
        super().__init__(request)

    def create_product(self):
        return self._CREATE_PRODUCT_PATH

    def create_product_api_payload(self, product: CreateProduct | None = None, **overrides) -> dict:
        """
        Build the create-product request body from the CreateProduct POJO.
        Default values from the POJO are used unless overridden.

        Args:
            product: A ready-made CreateProduct. Defaults are used if not given.
            **overrides: Individual fields to change, e.g. productPrice="999".

        Returns:
            dict: Request body for _CREATE_PRODUCT_PATH.
        """
        product = replace(product or CreateProduct(), **overrides)
        return product.to_multipart()
