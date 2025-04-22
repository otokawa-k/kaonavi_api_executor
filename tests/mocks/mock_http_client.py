class MockResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text

    def raise_for_status(self): pass

    def json(self):
        return self._json_data


class MockHttpClient:
    def __init__(self, mock_response=None):
        self._mock_response = mock_response or MockResponse(
            status_code=200,
            json_data={"access_token": "mocked-token"},
        )

    def post(self, url, data, headers=None, auth=None):
        return self._mock_response
