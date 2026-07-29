from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        if self.browser is not None:
            return self.page

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

        return self.page

    def current_page(self):

        if self.page is None:
            self.start()

        return self.page

    def open_url(self, url):

        page = self.current_page()

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        page.goto(url)

        return page

    def close(self):

        if self.browser:

            self.browser.close()

            self.playwright.stop()

            self.browser = None
            self.context = None
            self.page = None
            self.playwright = None