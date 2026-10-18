from api.api_base import ApiBase
from pojo.create_order import CreateOrder, Order


class CreateOrderApi(ApiBase):
    _CREATE_ORDER_PATH = "api/ecom/order/create-order"
    _PAYLOAD_FILE = "create_order_api.json"

    def __init__(self, request):
        super().__init__(request)

    def create_order(self):
        return self._CREATE_ORDER_PATH

    def create_order_api_payload_json(self, product_id: str) -> dict:
        """
        Build the create-order request body from data/create_order_api.json.
        Values from the file are used unless overridden here.

        Returns:
            dict: Request body for CREATE_ORDER_PATH.
        """
        _payload = self.load_payload(self._PAYLOAD_FILE)
        _payload["orders"][0]["productOrderedId"] = product_id
        return _payload

    def create_order_api_payload_pojo(self, product_ids: list[str], country: str = "India") -> dict:
        """
        Build the create-order request body from the CreateOrder POJO.

        Args:
            product_ids: productIds to order (one order entry per product).
            country: Delivery country for every order entry.

        Returns:
            dict: Request body for _CREATE_ORDER_PATH.
        """
        order = CreateOrder(
            orders=[Order(country=country, productOrderedId=pid) for pid in product_ids]
        )
        return order.to_dict()
