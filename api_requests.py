from httpx import AsyncClient, HTTPStatusError, RequestError

from exceptions import WeatherstackAPIError

WEATHERSTACK_BASE_URL = "http://api.weatherstack.com"


async def _safe_request(
    method: str,
    url: str,
    **kwargs: dict,
) -> dict:
    async with AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except HTTPStatusError as e:
            raise WeatherstackAPIError(
                f"API error {e.response.status_code} at {url}: {e.response.text}"
            ) from e

        except RequestError as e:
            raise WeatherstackAPIError(
                f"Network error during request to {url}: {str(e)}"
            ) from e

        except Exception as e:
            raise WeatherstackAPIError(
                f"Unexpected error during request to {url}: {str(e)}"
            ) from e


async def get_current_weather(query: str, api_key: str) -> dict:
    url = f"{WEATHERSTACK_BASE_URL}/current"
    params = {"access_key": api_key, "query": query}
    return await _safe_request("GET", url, params=params)


async def get_historical_weather(query: str, historical_date: str, api_key: str):
    url = f"{WEATHERSTACK_BASE_URL}/historical"
    params = {
        "access_key": api_key,
        "query": query,
        "historical_date": historical_date,
    }
    return await _safe_request("GET", url, params=params)
