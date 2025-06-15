import unittest
from unittest.mock import patch, MagicMock
from backend.bedrock_client import call_model

class TestBedrockClient(unittest.TestCase):

    @patch("backend.bedrock_client.bedrock")
    def test_call_model_returns_output_and_duration(self, mock_bedrock):
        # Mock the nested structure: response["body"].read().decode()
        fake_output_text = "Hello from Bedrock!"
        mock_body = MagicMock()
        mock_body.read.return_value = json_bytes = bytes(
            json_string := '{"results": [{"outputText": "' + fake_output_text + '"}]}',
            encoding='utf-8'
        )
        mock_bedrock.invoke_model.return_value = {"body": mock_body}

        result, duration = call_model("Hi!")

        self.assertEqual(result, fake_output_text)
        self.assertIsInstance(duration, float)
        self.assertLess(duration, 1.0)  # should run fast with mocks

        mock_bedrock.invoke_model.assert_called_once()
        args, kwargs = mock_bedrock.invoke_model.call_args
        self.assertEqual(kwargs["modelId"], "amazon.titan-tg1-large")

if __name__ == "__main__":
    unittest.main()
