import pytest
from api.delete_product_api import DeleteProductApi
from config.config import APIPRODUCTDELETEMESSAGE
from tests.base_test import BaseTest, log_information, assert_http_ok, assert_equal


class TestDeleteProductApi(BaseTest):

    @pytest.mark.api
    @pytest.mark.description("Verify a product can be deleted by its creator.")
    @pytest.mark.major
    @pytest.mark.skip_teardown
    def test_delete_product_api(self, auth, create_product):
        """@priority P3 @owner Shantanu @feature delete_order_api"""
        log_information("Delete the created product")
        _delete_api = DeleteProductApi(auth.context)
        _delete_response = _delete_api.submit_delete_api(url=_delete_api.delete_product_path(create_product),
                                                         headers={"Authorization": auth.token})

        log_information("Verify the delete product response")
        assert_http_ok("Verify the delete product response.", _delete_response)
        assert_equal("Verify the product is deleted.", APIPRODUCTDELETEMESSAGE,
                     _delete_response.json()["message"])