import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import Request
import re
import io
from contextlib import redirect_stdout
import asyncio

from backend.monitor import log_middleware

class TestLogMiddleware(unittest.TestCase):

    def test_log_middleware_timing_and_output(self):
        # Create a fake FastAPI Request object
        mock_request = MagicMock(spec=Request)
        mock_request.url.path = "/chat"

        # Create a mocked response from downstream route
        mock_response = MagicMock()
        mock_call_next = AsyncMock(return_value=mock_response)

        # Capture printed output
        f = io.StringIO()
        with redirect_stdout(f):
            asyncio.run(log_middleware(mock_request, mock_call_next))

        output = f.getvalue()

        # Check that call_next was called with the request
        mock_call_next.assert_awaited_once_with(mock_request)

        # Check that monitor message was printed correctly
        self.assertRegex(output, r"\[MONITOR\] /chat took \d+\.\d{2}s")

if __name__ == "__main__":
    unittest.main()
