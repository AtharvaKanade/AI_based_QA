"""
Base Page Class for Page Object Model (POM) Pattern.
Provides common navigation and element interaction wrappers using Playwright.
"""

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

