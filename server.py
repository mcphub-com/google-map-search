import os, requests
from datetime import datetime
from typing import Union, Literal, List
from mcp.server import FastMCP
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP('serp-map')


serp_url = "https://serpapi.com/search"
serp_api_key = os.getenv("SERP_API_KEY")

@mcp.tool()
def search_map(q: Annotated[str, Field(description='Parameter defines the query you want to search. You can use anything that you would use in a regular Google Maps search.')],
                ll: Annotated[Union[str, None], Field(description='Parameter defines the GPS coordinates of the location where you want the search to originate from. Its value must match the following format: @ + latitude + , + longitude + , + zoom. This will form a string that looks like this:  e.g. @40.7455096,-74.0083012,14z. The zoom attribute ranges from 3z, map completely zoomed out - to 21z, map completely zoomed in. The parameter should only be used when type is set to search.')] = None,
                start: Annotated[Union[int, None], Field(description="Parameter defines the result offset. It skips the given number of results. It's used for pagination. On desktop, parameter only accepts multiples of 20 (e.g. 20 for the second page results, 40 for the third page results, etc.). On mobile, parameter only accepts multiples of 10 (e.g. 10 for the second page results, 20 for the third page results, etc.).")] = None,
                no_cache: Annotated[Union[bool, None], Field(description="Parameter will force SerpApi to fetch the Google Jobs results even if a cached version is already present. A cache is served only if the query and all parameters are exactly the same. Cache expires after 1h. Cached searches are free, and are not counted towards your searches per month. It can be set to false (default) to allow results from the cache, or true to disallow results from the cache. no_cache and async parameters should not be used together.")] = None,
                aasync: Annotated[Union[bool, None], Field(description="Parameter defines the way you want to submit your search to SerpApi. It can be set to false (default) to open an HTTP connection and keep it open until you got your search results, or true to just submit your search to SerpApi and retrieve them later. In this case, you'll need to use our Searches Archive API to retrieve your results. async and no_cache parameters should not be used together. async should not be used on accounts with Ludicrous Speed enabled.")] = None
            ):
    '''This tool allows you to Scrape Google Maps data.'''
    payload = {
        'q': q,
        'engine': "google_maps",
        'api_key': serp_api_key,
        'type': "search",
        'll': ll,
        "start": start,
        "no_cache": no_cache,
        "async": aasync
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    print(payload)

    response = requests.get(serp_url, params=payload)
    print(response)
    return response.json()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")