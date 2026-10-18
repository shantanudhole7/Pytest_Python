import pytest
from api.create_order_api import CreateOrderApi
from api.create_product_api import CreateProductApi
from config.config import APIORDERPLACEDMESSAGE
from tests.base_test import BaseTest, log_information, assert_http_ok, assert_equal


class TestCreateOrderApi(BaseTest):

    @pytest.mark.description("Verify an order can be created from the JSON payload.")
    @pytest.mark.api
    @pytest.mark.critical
    def test_create_order_json_api(self, auth, create_product):
        """@priority P2 @owner Shantanu @feature create_order_api"""
        log_information("Build the order Api with created product")
        _order_api = CreateOrderApi(auth.context)
        _order_payload = _order_api.create_order_api_payload_json(create_product)
        _order_response = _order_api.submit_post_api(url=_order_api.create_order(), data=_order_payload,
                                                     headers={"Authorization": auth.token})

        log_information("Verify the create order response")
        assert_http_ok("Verify the create order response.", _order_response)
        assert_equal("Verify the order is placed.", APIORDERPLACEDMESSAGE, _order_response.json()["message"])

    @pytest.mark.description("Verify an order can be created from the POJO class file")
    @pytest.mark.api
    @pytest.mark.critical
    def test_create_order_pojo_api(self, auth, create_product):
        """@priority P2 @owner Shantanu @feature create_order_api"""
        log_information("Build the order Api with created product")
        _order_api = CreateOrderApi(auth.context)
        _order_payload = _order_api.create_order_api_payload_pojo([create_product])
        _order_response = _order_api.submit_post_api(url=_order_api.create_order(), data=_order_payload,
                                                     headers={"Authorization": auth.token})

        log_information("Verify the create order response")
        assert_http_ok("Verify the create order response.", _order_response)
        assert_equal("Verify the order is placed.", APIORDERPLACEDMESSAGE, _order_response.json()["message"])

    @pytest.mark.description("Verify an order with two products can be created.")
    @pytest.mark.api
    @pytest.mark.major
    def test_create_order_api_multiple_product(self, auth, create_product, delete_product):
        """@priority P3 @owner Shantanu @feature create_order_api"""
        log_information("Create a second product")
        _product_api = CreateProductApi(auth.context)
        _product_payload = _product_api.create_product_api_payload(productAddedBy=auth.user_id)
        _product_response = _product_api.submit_post_api(url=_product_api.create_product(), multipart=_product_payload,
                                                      headers={"Authorization": auth.token})

        log_information("Verify the second product is created.")
        assert_http_ok("Verify the second product is created.", _product_response)


        log_information("Take product from response and add clean up code for delete product")
        _product_id_1 = _product_response.json()["productId"]
        delete_product.append(_product_id_1)

        log_information("Build the order payload for both products")
        _product_ids = [create_product, _product_id_1]
        _order_api = CreateOrderApi(auth.context)
        _order_payload = _order_api.create_order_api_payload_pojo(_product_ids)

        log_information("Create order api for 2 products")
        _order_response = _order_api.submit_post_api(url=_order_api.create_order(), data=_order_payload,
                                                     headers={"Authorization": auth.token})

        log_information("Verify the create order response")
        assert_http_ok("Verify the create order response.", _order_response)
        assert_equal("Verify two orders are created.", len(_product_ids), len(_order_response.json()["orders"]))
        assert_equal("Verify the order is placed.", APIORDERPLACEDMESSAGE, _order_response.json()["message"])
