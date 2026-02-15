"""
Browser Service - Web automation using Playwright.

Ported from OpenClaw browser functionality.
"""

import os
import base64
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Page, Browser


class BrowserService:
    """Web browser automation service."""
    
    def __init__(self, headless: bool = True, screenshot_dir: str = "/tmp/busy38/screenshots"):
        self.headless = headless
        self.screenshot_dir = screenshot_dir
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
        # Ensure screenshot directory exists
        os.makedirs(screenshot_dir, exist_ok=True)
    
    async def initialize(self):
        """Initialize Playwright browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        
        # Set viewport
        await self.page.set_viewport_size({"width": 1280, "height": 720})
    
    async def close(self):
        """Close browser and cleanup."""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to URL."""
        if not self.page:
            return {"success": False, "error": "Browser not initialized"}
        
        try:
            response = await self.page.goto(url, wait_until="networkidle")
            
            return {
                "success": True,
                "url": self.page.url,
                "title": await self.page.title(),
                "status": response.status if response else None
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def screenshot(self, selector: Optional[str] = None) -> Dict[str, Any]:
        """Capture screenshot."""
        if not self.page:
            return {"success": False, "error": "Browser not initialized"}
        
        try:
            if selector:
                # Screenshot specific element
                element = await self.page.query_selector(selector)
                if not element:
                    return {"success": False, "error": f"Element not found: {selector}"}
                screenshot_bytes = await element.screenshot()
            else:
                # Full page screenshot
                screenshot_bytes = await self.page.screenshot(full_page=True)
            
            # Encode as base64
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode()
            
            # Save to file
            filename = f"screenshot_{self.page.url.replace('/', '_')[:50]}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            with open(filepath, "wb") as f:
                f.write(screenshot_bytes)
            
            return {
                "success": True,
                "screenshot_base64": screenshot_b64,
                "filepath": filepath,
                "url": self.page.url
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def click(self, selector: str) -> Dict[str, Any]:
        """Click element."""
        if not self.page:
            return {"success": False, "error": "Browser not initialized"}
        
        try:
            await self.page.click(selector)
            return {
                "success": True,
                "action": "click",
                "selector": selector,
                "url": self.page.url
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def type_text(self, selector: str, text: str) -> Dict[str, Any]:
        """Type text into input."""
        if not self.page:
            return {"success": False, "error": "Browser not initialized"}
        
        try:
            await self.page.fill(selector, text)
            return {
                "success": True,
                "action": "type",
                "selector": selector,
                "text_length": len(text)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def evaluate(self, javascript: str) -> Dict[str, Any]:
        """Execute JavaScript."""
        if not self.page:
            return {"success": False, "error": "Browser not initialized"}
        
        try:
            result = await self.page.evaluate(javascript)
            return {
                "success": True,
                "result": result,
                "javascript": javascript[:100] + "..." if len(javascript) > 100 else javascript
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def extract_text(self, selector: str = "body") -> Dict[str, Any]:
        """Extract text content from selector."""
        if not self.page:
            return {"success": False, "error": "Browser not initialized"}
        
        try:
            element = await self.page.query_selector(selector)
            if not element:
                return {"success": False, "error": f"Element not found: {selector}"}
            
            text = await element.inner_text()
            
            return {
                "success": True,
                "selector": selector,
                "text": text,
                "length": len(text)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_page_content(self) -> Dict[str, Any]:
        """Get full page content."""
        if not self.page:
            return {"success": False, "error": "Browser not initialized"}
        
        try:
            html = await self.page.content()
            text = await self.page.inner_text("body")
            title = await self.page.title()
            
            return {
                "success": True,
                "url": self.page.url,
                "title": title,
                "html": html,
                "text": text
            }
        except Exception as e:
            return {"success": False, "error": str(e)}