import requests
from typing import Any, Tuple, Union, Literal


class ApiCalls:
    base_url = None
    timeout = 400

    def is_http_url(self, url: str):
        return url.startswith("http://") or url.startswith("https://")

    def _extract_response(self, response: requests.Response):
        try:
            return response.json()
        except:
            return response.text

    def _append_url(self, url: str):
        if self.base_url:
            if self.base_url.endswith("/"):
                if url.startswith("/"):
                    url = url[1:]
                return self.base_url + url
            if url.startswith("/"):
                return self.base_url + url
            return self.base_url + "/" + url
        raise Exception("Base url is not provided!")

    def make_request(self,
                     url: str, method: Literal["get", "post", "patch", "delete"],
                     params: Union[dict, None] = None, data: Union[dict, None] = None,
                     use_json=True) -> Tuple[Any, Union[str, None]]:
        """
        Make a request to the specified URL using the given HTTP method.

        Args:
            url (str): The URL to make the request to.
            method (Literal["get", "post", "patch", "delete"]): The HTTP method to use for the request.
            params (Union[dict, None], optional): The query parameters to include in the request URL.
            data (Union[dict, None], optional): The data to include in the request body.
            use_json (bool, optional): Whether to use JSON format for the request body. Default is True.

        Returns:
            Tuple[Any, Union[str, None]]: A tuple containing the response data and any error message.
                - The response data can be of any type.
                - If an error occurs during the request, an error message will be provided.
                - If no error occurs, the error message will be None.
        """
        def get_required_call():
            if method == "get":
                return requests.get
            elif method == "post":
                return requests.post
            elif method == "delete":
                return requests.delete
            elif method == "patch":
                return requests.patch
            else:
                raise Exception(
                    'Method should be in ["get", "post", "patch", "delete"]')

        call = get_required_call()
        url = self._get_full_url(url)
        parameters = {
            "url": url,
            "timeout": self.timeout,
        }
        if data:
            if use_json:
                parameters["json"] = data
            else:
                parameters["data"] = data
        if params:
            parameters["params"] = params
        response = call(**parameters)
        if response.ok:
            return self._extract_response(response), None
        return None, self._extract_response(response)

    def _get_full_url(self, url: Union[str, None] = None):
        _url = None
        is_http_url = self.is_http_url(url)
        if is_http_url:
            _url = url
        else:
            if self.base_url:
                _url = self._append_url(url)
            else:
                raise Exception(
                    "Invalid url provided. Please provide a valid url or a base url")
        return _url
