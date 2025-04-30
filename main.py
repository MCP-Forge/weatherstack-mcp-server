from typing import Union

from mcp.server.fastmcp import Context
from mcp.types import CallToolResult, TextContent

from config import mcp
from exceptions import WeatherstackAPIError
from api_requests import get_current_weather, get_historical_weather


@mcp.tool()
async def query_current_weather(
    query: str, ctx: Context
) -> Union[dict, CallToolResult]:
    """
    Gets the current weather for a specified location using the Weatherstack API.

    Parameters:
        query (str): The location to retrieve weather data for.
            Supported formats:
            - City name (e.g. "New York")
            - ZIP code (UK, Canada, US) (e.g. "99501")
            - Latitude,Longitude coordinates (e.g. "40.7831,-73.9712")
            - IP address (e.g. "153.65.8.20")
            - Special keyword "fetch:ip" to auto-detect requester IP

    Returns:
        Union[dict, CallToolResult]: A dictionary containing the current weather data,
        or a CallToolResult with an error message if the request fails.
    """
    api_key = ctx.request_context.lifespan_context.api_key

    try:
        data = await get_current_weather(query, api_key)
    except WeatherstackAPIError as e:
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Weatherstack API Error {e}")],
        )

    return data


@mcp.tool()
async def query_historical_weather(
    query: str, historical_dates: list[str], ctx: Context
) -> Union[dict, CallToolResult]:
    """
    Gets historical weather data for a specified location and list of dates using the Weatherstack API.

    Parameters:
        query (str): The location to retrieve weather data for.
            Supported formats:
            - City name (e.g. "New York")
            - ZIP code (UK, Canada, US) (e.g. "99501")
            - Latitude,Longitude coordinates (e.g. "40.7831,-73.9712")
            - IP address (e.g. "153.65.8.20")
            - Special keyword "fetch:ip" to auto-detect requester IP
        historical_dates (list[str]): A list of historical dates in 'YYYY-MM-DD' format.

    Returns:
        Union[dict, CallToolResult]: A dictionary containing the historical weather data,
        or a CallToolResult with an error message if the request fails.
    """

    api_key = ctx.request_context.lifespan_context.api_key

    try:
        historical_dates_str = ";".join(historical_dates)
        data = await get_historical_weather(query, historical_dates_str, api_key)
    except WeatherstackAPIError as e:
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Weatherstack API Error {e}")],
        )

    return data


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
