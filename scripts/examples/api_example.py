import asyncio
import json
import logging
from urllib.parse import urlparse
from crawl4ai.docker_client import Crawl4aiDockerClient
from crawl4ai import  CacheMode # Assuming you have crawl4ai installed
from .ai2_policy import Ai2BotConfig


logger = logging.getLogger(__name__)

class Crawl4aiApiClient(Crawl4aiDockerClient):

    def __init__(self, base_url: str, *args, **kwargs):
        super().__init__(base_url=base_url, *args, **kwargs)
        self._path_url = urlparse(base_url).path

    async def _check_server(self) -> None:
        """Check if server is reachable, raising an error if not."""
        try:
            await self._http_client.get(f"{self.base_url}{self._path_url}/health")
            self.logger.success(f"Connected to {self.base_url}", tag="READY")
        except Exception as e:
            self.logger.error(f"Server unreachable: {str(e)}", tag="ERROR")
            raise ConnectionError(f"Cannot connect to server: {str(e)}")

    async def authenticate(self, api_key: str) -> None:
        self._http_client.headers["x-api-key"] = api_key

    def _request(self, method: str, endpoint: str, **kwargs):
        return super()._request(method, self._path_url + endpoint, **kwargs)


async def main():
    ai2_bot_config = Ai2BotConfig()

    # Point to the correct server port
    async with Crawl4aiApiClient(base_url=ai2_bot_config.get_base_url(), verbose=True) as client:
        # slightly different authentication method; no email; just API key
        await client.authenticate(ai2_bot_config.get_api_key())

        # Example Non-streaming crawl
        print("--- Running Non-Streaming Crawl ---")
        results = await client.crawl(
            ["https://httpbin.org/html"],
            browser_config=ai2_bot_config.get_browser_config(),
            crawler_config=ai2_bot_config.get_crawler_config(cache_mode=CacheMode.BYPASS)
        )

        if results: # client.crawl returns None on failure
            if not isinstance(results, list):
                results = [results]
            for result in results: # Iterate through the CrawlResultContainer
                result_json = json.loads(result.model_dump_json()) # type: ignore
                print(f"URL: {result_json['url']}, Success: {result_json['success']}")
        else:
            print("Non-streaming crawl failed.")


        # Example Streaming crawl
        print("\n--- Running Streaming Crawl ---")
        stream_config = ai2_bot_config.get_crawler_config(stream=True, cache_mode=CacheMode.BYPASS)
        try:
            async for result in await client.crawl(
                ["https://httpbin.org/html", "https://httpbin.org/links/5/0"],
                browser_config=ai2_bot_config.get_browser_config(),
                crawler_config=stream_config
            ): # type: ignore
                print(f"Streamed result: URL: {result.url}, Success: {result.success}")
        except Exception as e:
            print(f"Streaming crawl failed: {e}")


        # Example Get schema
        print("\n--- Getting Schema ---")
        schema = await client.get_schema()
        print(f"Schema received: {bool(schema)}") # Print whether schema was received

if __name__ == "__main__":
    asyncio.run(main())
