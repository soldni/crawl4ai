import os
from dataclasses import dataclass, field
from crawl4ai import BrowserConfig, CrawlerRunConfig


@dataclass(frozen=True)
class Ai2BotConfig:
    base_url: str | None = field(default_factory=lambda: os.getenv("CRAWL4AI_API_URL"))
    api_key: str | None = field(default_factory=lambda: os.getenv("CRAWL4AI_API_KEY"))
    blocklist_path: str | None = field(default_factory=lambda: os.getenv("CRAWL4AI_BLOCKLIST_PATH"))

    user_agent: str = "Mozilla/5.0 (compatible) AI2Bot-DeepResearchEval (+https://www.allenai.org/crawler)"
    headless: bool = True
    browser_mode: str = "dedicated"
    use_managed_browser: bool = False
    user_agent_mode: str = ""
    user_agent_generator_config: dict = field(default_factory=lambda: {})
    extra_args: list = field(default_factory=lambda: [])
    enable_stealth: bool = False
    check_robots_txt: bool = True
    semaphore_count: int = 50 # no more than 50

    def get_exclude_domains(self) -> list:
        if self.blocklist_path is None:
            raise ValueError(
                "CRAWL4AI_BLOCKLIST_PATH is not set; "
                "download the latest from from https://github.com/allenai/crawler-rules/blob/main/blocklist.txt"
            )
        if not os.path.exists(self.blocklist_path):
            raise FileNotFoundError(f"Blocklist file not found: {self.blocklist_path}")
        with open(self.blocklist_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    def get_browser_config(self, *args, **kwargs) -> BrowserConfig:
        return BrowserConfig(
            *args,
            headless=self.headless,
            user_agent=self.user_agent,
            browser_mode=self.browser_mode,
            use_managed_browser=self.use_managed_browser,
            user_agent_mode=self.user_agent_mode,
            user_agent_generator_config=self.user_agent_generator_config,
            extra_args=self.extra_args,
            enable_stealth=self.enable_stealth,
            **kwargs,
        )

    def get_crawler_config(self, *args, **kwargs) -> CrawlerRunConfig:
        return CrawlerRunConfig(
            *args,
            check_robots_txt=self.check_robots_txt,
            exclude_domains=self.get_exclude_domains(),
            geolocation=None,
            timezone_id=None,
            locale=None,
            simulate_user=False,
            semaphore_count=self.semaphore_count,
            user_agent=self.user_agent,
            user_agent_mode=self.user_agent_mode,
            user_agent_generator_config=self.user_agent_generator_config,
            **kwargs,
        )

    def get_base_url(self) -> str:
        if self.base_url is None:
            raise ValueError("CRAWL4AI_API_URL is not set")
        return self.base_url

    def get_api_key(self) -> str:
        if self.api_key is None:
            raise ValueError("CRAWL4AI_API_KEY is not set")
        return self.api_key
