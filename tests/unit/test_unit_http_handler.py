import pytest
from fastapi import Response, status
from app.handler_http import root, fail


@pytest.mark.unit
class TestHttpHandlerUnit:
    def test_root(self):
        # Test the root endpoint
        result = root()
        assert result == {"message": "OK"}

    def test_fail(self):
        # Test the fail endpoint
        response = Response()
        result = fail(response)
        assert result == {"message": "failure"}
        assert response.status_code == status.HTTP_400_BAD_REQUEST
