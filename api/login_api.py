from api.api_base import ApiBase
from config.config import APIUSEREMAIL, APIUSERPASSWORD


class LoginApi(ApiBase):
    """Login endpoint: provides the path and request body; the test sends the request."""

    _LOGIN_PATH = "/api/ecom/auth/login"

    def __init__(self, request):
        super().__init__(request)

    def login(self):
        return self._LOGIN_PATH

    def login_api_payload(self) -> dict:
        """
        Build the login request body.

        Returns:
            dict: Request body for LOGIN_PATH.
        """
        return {"userEmail": APIUSEREMAIL, "userPassword": APIUSERPASSWORD}
