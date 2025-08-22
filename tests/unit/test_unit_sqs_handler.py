import pytest
import json
from unittest.mock import patch
from app.handler_sqs import handler

@pytest.mark.unit
class TestSqsHandlerUnit:
    def test_handler_valid_sns_message(self):
        # Mock event with a single SNS message
        event = {
            "Records": [
                {
                    "Sns": {
                        "Message": json.dumps({"key": "value"})
                    }
                }
            ]
        }
        context = {}  # Mock context (not used in handler)
        
        with patch("builtins.print") as mock_print:
            result = handler(event, context)
            mock_print.assert_called_once_with("Processing SNS message: " + json.dumps({"key": "value"}))
            assert result == {"statusCode": 200}

    def test_handler_empty_records(self):
        # Test with empty Records list
        event = {
            "Records": []
        }
        context = {}
        
        with patch("builtins.print") as mock_print:
            result = handler(event, context)
            mock_print.assert_not_called()
            assert result == {"statusCode": 200}
