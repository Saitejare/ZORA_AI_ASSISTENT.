from pathlib import Path

from playwright.sync_api import sync_playwright

from .session_manager import BrowserSessionManager


class BrowserManager:

    def __init__(self):

        self.playwright = None

        self.browser = None

        self.session = BrowserSessionManager()

    # -----------------------------------------------------

    def start(self):

        if self.session.has_page():

            return self.session.get_page()

        if self.playwright is None:

            self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch_persistent_context(

            user_data_dir=str(
                Path(__file__).resolve().parents[2]
                / "browser_profile"
            ),

            channel="chrome",

            headless=False,

        )

        self.session.set_context(self.browser)

        if self.browser.pages:

            page = self.browser.pages[0]

        else:

            page = self.browser.new_page()

        self.session.set_page(page)

        return page

    # -----------------------------------------------------

    def current_page(self):

        if not self.session.has_page():

            return self.start()

        return self.session.get_page()

    # -----------------------------------------------------

    def open_url(self, url):

        page = self.current_page()

        if not url.startswith(("http://", "https://")):

            url = "https://" + url

        page.goto(

            url,

            wait_until="domcontentloaded",

        )

        return page

    # -----------------------------------------------------

    def new_page(self):

        context = self.session.get_context()

        if context is None:

            self.start()

            context = self.session.get_context()

        page = context.new_page()

        self.session.set_page(page)

        return page

    # -----------------------------------------------------

    def close(self):

        context = self.session.get_context()

        if context:

            context.close()

        self.session.clear()

        if self.playwright:

            self.playwright.stop()

            self.playwright = None

        self.browser = None
