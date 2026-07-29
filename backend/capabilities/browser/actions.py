from .browser_manager import BrowserManager
from .search_engine import SearchEngine
from .page_reader import PageReader
from .downloader import Downloader
from .tab_manager import TabManager


class BrowserActions:

    def __init__(self):

        self.browser = BrowserManager()

        self.browser.start()

        self.search = SearchEngine()

        self.tabs = TabManager(self.browser.context)

    # --------------------------------------------------
    # URL
    # --------------------------------------------------

    def open_url(self, url):

        url = self.search.normalize_url(url)

        self.browser.open_url(url)

        return f"Opened {url}"

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search_web(
        self,
        query,
        engine="google"
    ):

        url = self.search.build_search_url(
            query,
            engine
        )

        self.browser.open_url(url)

        return f"Searching '{query}' using {engine}"

    # --------------------------------------------------
    # Reader
    # --------------------------------------------------

    def page_reader(self):

        return PageReader(
            self.browser.current_page()
        )

    def page_title(self):

        return self.page_reader().title()

    def page_text(self):

        return self.page_reader().text()

    def page_metadata(self):

        return self.page_reader().metadata()

    # --------------------------------------------------
    # Tabs
    # --------------------------------------------------

    def new_tab(self):

        self.tabs.new_tab()

        return "New tab opened."

    def list_tabs(self):

        return self.tabs.list_tabs()

    def switch_tab(self, index):

        self.tabs.switch_tab(index)

        return f"Switched to tab {index}"

    def close_current_tab(self):

        self.tabs.close_current_tab()

        return "Current tab closed."

    # --------------------------------------------------
    # Downloader
    # --------------------------------------------------

    def downloader(self):

        return Downloader(
            self.browser.current_page()
        )

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    def close_browser(self):

        self.browser.close()

        return "Browser closed."