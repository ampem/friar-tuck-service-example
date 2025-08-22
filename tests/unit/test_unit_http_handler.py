import pytest
from fastapi import Response, status
from app.handler_http import root, fail


def test_root():
    # Test the root endpoint
    result = root()
    assert result == {"message": "OK"}


def test_fail():
    # Test the fail endpoint
    response = Response()
    result = fail(response)
    assert result == {"message": "Failure"}
    assert response.status_code == status.HTTP_400_BAD_REQUEST
