from dataclasses import dataclass
import pytest
from playwright.sync_api import APIRequestContext
from api.create_product_api import CreateProductApi
from api.delete_product_api import DeleteProductApi
from api.login_api import LoginApi
from config.config import APIBASEURL


@dataclass(frozen=True)
class Auth:
    context: APIRequestContext
    token: str
    user_id: str


@pytest.fixture(scope="session")
def api_context(playwright):
    """
    One request context for the whole run, pointed at APIBASEURL, closed at the end.
    """
    _context = playwright.request.new_context(
        base_url=APIBASEURL,
        extra_http_headers={"Accept": "application/json"},
    )
    yield _context
    _context.dispose()


@pytest.fixture(scope="session")
def auth(api_context) -> Auth:
    """
    Log in once per run

    Returns:
        Return the token and userId
    """
    login_api = LoginApi(api_context)
    response = login_api.submit_post_api(url=login_api.login(), data=login_api.login_api_payload())
    assert response.ok, f"Login failed: {response.text()}"
    _body = response.json()
    yield Auth(context=api_context, token=_body["token"], user_id=_body["userId"])


@pytest.fixture
def create_product(auth, delete_product) -> str:
    """
    Create a product and return its productId and last clean up.

    Returns:
        Return the product id
    """
    product_api = CreateProductApi(auth.context)
    payload = product_api.create_product_api_payload(productAddedBy=auth.user_id)
    response = product_api.submit_post_api(
        url=product_api.create_product(),
        multipart=payload,
        headers={"Authorization": auth.token},
    )
    assert response.ok, f"Create product failed: {response.text()}"
    yield response.json()["productId"]
    delete_product.append(response.json()["productId"])


@pytest.fixture
def delete_product(auth, request):
    """
    Delete a product for cleanup purposes.
    """
    _product_ids = []
    yield _product_ids
    if request.node.get_closest_marker("skip_teardown"):
        return
    _delete_api = DeleteProductApi(auth.context)
    for _product_id in _product_ids:
        _response = _delete_api.submit_delete_api(url=_delete_api.delete_product_path(_product_id),
                                                  headers={"Authorization": auth.token})
        assert _response.ok, f"Delete failed: {_response.text()}"
