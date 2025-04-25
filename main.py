from typing import Union

from mcp.server.fastmcp import Context
from mcp.types import CallToolResult, TextContent

from config import mcp
from exceptions import WeatherstackAPIError
from api_requests import get_current_weather


@mcp.tool()
async def query_current_weather(
    query: str, ctx: Context
) -> Union[dict, CallToolResult]:
    """
    Gets the current weather for a location using the Weatherstack API.

    Supported location identifiers:
    - City name (e.g. "New York")
    - ZIP code (UK, Canada, US) (e.g. "99501")
    - Latitude,Longitude coordinates (e.g. "40.7831,-73.9712")
    - IP address (e.g. "153.65.8.20")
    - Special keyword "fetch:ip" to auto-detect requester IP

    Returns:
        A dictonary, containing the response.
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


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
