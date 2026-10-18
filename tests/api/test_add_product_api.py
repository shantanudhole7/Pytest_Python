import pytest
from api.create_product_api import CreateProductApi
from config.config import APIPRODUCTADDEDMESSAGE
from tests.base_test import BaseTest, log_information, assert_http_ok, assert_equal


class TestAddProductApi(BaseTest):

    @pytest.mark.description("Verify a product can be created for a logged-in user.")
    @pytest.mark.api
    @pytest.mark.critical
    def test_add_product_api(self, auth, delete_product):
        """@priority P2 @owner Shantanu @feature add_product_api"""
        log_information("Create a product for the logged-in user")
        _product_api = CreateProductApi(auth.context)
        _product_payload = _product_api.create_product_api_payload(productAddedBy=auth.user_id)
        _product_response = _product_api.submit_post_api(url=_product_api.create_product(), multipart=_product_payload,
                                                         headers={"Authorization": auth.token})

        log_information("Verify the create product response")
        assert_http_ok("Verify the create product response.", _product_response)

        log_information("Register the created product for cleanup")
        delete_product.append(_product_response.json()["productId"])

        log_information("Verify the product added message")
        assert_equal("Verify the successful create product.", APIPRODUCTADDEDMESSAGE,
                     _product_response.json()["message"])