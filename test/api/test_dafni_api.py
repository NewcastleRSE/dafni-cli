import pytest
from mock import patch
from requests.exceptions import HTTPError

from dafni_cli.consts import MODELS_API_URL
from dafni_cli.api import dafni_api
from test.fixtures.jwt_fixtures import request_response_fixture, JWT


@patch("dafni_cli.api.dafni_api.requests")
class TestDafniGetRequest:
    """Test class to test the dafni_get_request functionality"""

    def test_requests_response_processed_correctly(
        self, mock_request, request_response_fixture
    ):

        # SETUP
        # setup return value for requests call
        mock_request.get.return_value = request_response_fixture
        # setup data for call
        url = "dafni/models/url"
        jwt = JWT

        # CALL
        result = dafni_api.dafni_get_request(url, jwt)

        # ASSERT
        assert result == {"key": "value"}
        mock_request.get.assert_called_once_with(
            url,
            headers={"Content-Type": "application/json", "authorization": jwt},
            allow_redirects=False,
        )

    def test_exception_raised_for_failed_call(
        self, mock_request, request_response_fixture
    ):

        # SETUP
        # setup return value for requests call
        request_response_fixture.raise_for_status.side_effect = HTTPError(
            "404 client model"
        )
        mock_request.get.return_value = request_response_fixture

        # setup data for call
        url = "dafni/models/url"
        jwt = JWT

        # CALL
        # ASSERT
        with pytest.raises(HTTPError, match="404 client model"):
            dafni_api.dafni_get_request(url, jwt)
