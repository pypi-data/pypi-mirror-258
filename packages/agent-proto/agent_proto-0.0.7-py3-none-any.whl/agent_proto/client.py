"""
APIClient module: A general purpose asynchronous HTTP client for making requests.
"""

from __future__ import annotations

from typing import (
    Any,
    AsyncIterable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    TypeAlias,
    TypeVar,
    Union,
)

from httpx import AsyncClient
from pydantic import BaseModel

from .proxy import LazyProxy

T = TypeVar("T")
Method: TypeAlias = Literal[
    "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"
]
Json: TypeAlias = Union[Dict[str, "Json"], List["Json"], str, int, float, bool, None]
PrimitiveData: TypeAlias = Optional[Union[str, int, float, bool]]


class APIClient(BaseModel, LazyProxy[AsyncClient]):
    """
    A client for making HTTP requests asynchronously.

    Args:
        base_url (str): The base URL for the API.
        headers (Dict[str, str]): The headers to be included in the requests.

    Attributes:
        base_url (str): The base URL for the API.
        headers (Dict[str, str]): The headers to be included in the requests.
    """

    base_url: str
    headers: Dict[str, str]

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.__load__(*args, **kwargs)

    def __load__(self):
        return AsyncClient(base_url=self.base_url, headers=self.headers)

    def dict(self, *args: Any, **kwargs: Any):
        return super().model_dump(
            *args, **kwargs, exclude={"headers"}, exclude_none=True
        )

    def _update_headers(self, additional_headers: Optional[Dict[str, str]] = None):
        if additional_headers:
            self.headers.update(additional_headers)
        return self.headers

    async def fetch(
        self,
        url: str,
        method: Method,
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send an HTTP request asynchronously.

        Args:
            url (str): The URL for the request.
            method (Method): The HTTP method for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            json (Optional[Json]): The JSON payload for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        headers = self._update_headers(headers)
        return await self.__load__().request(
            method=method, url=url, headers=headers, json=json, params=params
        )

    async def get(
        self,
        url: str,
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send a GET request asynchronously.

        Args:
            url (str): The URL for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        response = await self.fetch(
            method="GET", url=url, headers=headers, params=params
        )
        return response.json()

    async def post(
        self,
        url: str,
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send a POST request asynchronously.

        Args:
            url (str): The URL for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            json (Optional[Json]): The JSON payload for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        response = await self.fetch(
            method="POST", url=url, json=json, headers=headers, params=params
        )
        return response.json()

    async def put(
        self,
        url: str,
        *,
        json: Optional[Json] = None,
        params: Optional[Dict[str, PrimitiveData]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send a PUT request asynchronously.

        Args:
            url (str): The URL for the request.
            json (Optional[Json]): The JSON payload for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        response = await self.fetch(
            method="PUT", url=url, json=json, headers=headers, params=params
        )
        return response.json()

    async def delete(
        self,
        url: str,
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send a DELETE request asynchronously.

        Args:
            url (str): The URL for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        response = await self.fetch(
            method="DELETE", url=url, headers=headers, params=params
        )
        return response.json()

    async def patch(
        self,
        url: str,
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send a PATCH request asynchronously.

        Args:
            url (str): The URL for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            json (Optional[Json]): The JSON payload for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        response = await self.fetch(
            method="PATCH", url=url, json=json, headers=headers, params=params
        )
        return response.json()

    async def head(
        self,
        url: str,
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send a HEAD request asynchronously.

        Args:
            url (str): The URL for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        response = await self.fetch(
            method="HEAD", url=url, headers=headers, params=params
        )
        return response.json()

    async def options(
        self,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send an OPTIONS request asynchronously.

        Args:
            url (str): The URL for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        response = await self.fetch(method="OPTIONS", url=url, headers=headers)
        return response.json()

    async def trace(
        self,
        url: str,
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send a TRACE request asynchronously.

        Args:
            url (str): The URL for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The JSON response from the request.
        """
        response = await self.fetch(
            method="TRACE", url=url, headers=headers, params=params
        )
        return response.json()

    async def text(
        self,
        url: str,
        method: Method = "GET",
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send an HTTP request asynchronously and return the response as text.

        Args:
            url (str): The URL for the request.
            method (Method): The HTTP method for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            json (Optional[Json]): The JSON payload for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The response content as text.
        """
        response = await self.fetch(
            method=method, url=url, json=json, headers=headers, params=params
        )
        return response.text

    async def blob(
        self,
        url: str,
        method: Method = "GET",
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> bytes:
        """
        Send an HTTP request asynchronously and return the response as binary data.

        Args:
            url (str): The URL for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            method (Method): The HTTP method for the request.
            json (Optional[Json]): The JSON payload for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            The response content as binary data.
        """
        response = await self.fetch(
            method=method, url=url, json=json, params=params, headers=headers
        )
        return response.content

    async def stream(
        self,
        url: str,
        method: Method = "GET",
        *,
        params: Optional[Dict[str, PrimitiveData]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
        mode: Literal["b", "s"] = "b",
        chunksize: int = 1024,
    ) -> AsyncIterable[bytes | str]:
        """
        Send an HTTP request asynchronously and stream the response.

        Args:
            url (str): The URL for the request.
            method (Method): The HTTP method for the request.
            params (Optional[Dict[str, PrimitiveData]]): The query parameters for the request.
            json (Optional[Json]): The JSON payload for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Yields:
            The response content as bytes in chunks.
        """
        headers = self._update_headers(headers)
        response = await self.fetch(
            url, method=method, json=json, params=params, headers=headers
        )
        async for chunk in response.aiter_bytes(chunk_size=chunksize):
            try:
                if mode == "s":
                    yield chunk.decode("utf-8")
                else:
                    yield chunk
            except StopAsyncIteration:
                break
            finally:
                response.close()

    async def upload(
        self,
        url: str,
        method: Method = "POST",
        *,
        data: (
            Dict[str, bytes]
            | Dict[str, AsyncIterable[bytes]]
            | Dict[str, Iterable[bytes]]
        ),
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send an HTTP request asynchronously to upload data.

        Args:
            url (str): The URL for the request.
            data (Dict[str, bytes] | Dict[str, AsyncIterable[bytes]] | Dict[str, Iterable[bytes]]): The data to be uploaded.
            method (Method): The HTTP method for the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.
        """
        assert method in ("POST", "PUT"), "Invalid method for upload request."
        headers = self._update_headers(headers)
        return await self.__load__().request(
            method=method, url=url, headers=headers, data=data
        )
