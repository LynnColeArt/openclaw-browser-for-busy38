"""
Busy38 Browser Plugin - OpenClaw Browser Port

Web automation and content extraction with security-first architecture.
"""

from .browser_service import BrowserService
from .content_screener import ContentScreener

__version__ = "0.1.0"
__all__ = ["BrowserService", "ContentScreener"]


class BrowserPlugin:
    """Main plugin entry point for Busy38 integration."""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.browser = None
        self.screener = ContentScreener()
    
    async def initialize(self):
        """Initialize the browser service."""
        self.browser = BrowserService(
            headless=self.config.get("headless", True),
            screenshot_dir=self.config.get("screenshot_dir", "/tmp/busy38/screenshots")
        )
        await self.browser.initialize()
    
    async def shutdown(self):
        """Graceful shutdown."""
        if self.browser:
            await self.browser.close()
    
    # Cheatcode handlers
    async def navigate(self, url: str) -> dict:
        """[browser:navigate <url>] - Navigate to URL."""
        return await self.browser.navigate(url)
    
    async def screenshot(self, selector: str = None) -> dict:
        """[browser:screenshot <selector?>] - Capture screenshot."""
        return await self.browser.screenshot(selector)
    
    async def click(self, selector: str) -> dict:
        """[browser:click <selector>] - Click element."""
        return await self.browser.click(selector)
    
    async def type_text(self, selector: str, text: str) -> dict:
        """[browser:type <selector> <text>] - Type text into input."""
        return await self.browser.type_text(selector, text)
    
    async def evaluate(self, javascript: str) -> dict:
        """[browser:eval <javascript>] - Execute JavaScript."""
        return await self.browser.evaluate(javascript)
    
    async def extract_text(self, selector: str = "body") -> dict:
        """[browser:text <selector?>] - Extract text content."""
        return await self.browser.extract_text(selector)
    
    async def get_content(self) -> dict:
        """[browser:content] - Get full page content with Toots screening."""
        content = await self.browser.get_page_content()
        
        # Screen through Toots
        screening = await self.screener.screen_content(content["html"])
        
        return {
            "url": content["url"],
            "title": content["title"],
            "text": content["text"],
            "html": content["html"],
            "screening": screening
        }