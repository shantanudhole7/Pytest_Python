from api.api_base import ApiBase


class DeleteProductApi(ApiBase):
    _DELETE_PRODUCT_PATH = "api/ecom/product/delete-product/{product_id}"

    def __init__(self, request):
        super().__init__(request)

    def delete_product_path(self, product_id: str) -> str:
        """
        Build the delete-product URL for the given product.

        Args:
            product_id: The productId returned by add-product.

        Returns:
            str: Path for the delete-product request.
        """
        return self._DELETE_PRODUCT_PATH.format(product_id=product_id)