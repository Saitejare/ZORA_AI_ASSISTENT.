import webbrowser

from .browser_manager import BrowserManager
from .search_engine import SearchEngine
from .page_reader import PageReader
from .downloader import Downloader
from .tab_manager import TabManager
from .website_resolver import WebsiteResolver
from .google_search import GoogleSearch
from .official_site import OfficialWebsiteFinder
from .context import BrowserContext


class BrowserActions:

    def __init__(self):
        self.context = BrowserContext()

        self.browser = BrowserManager()
        self.resolver = WebsiteResolver()
        self.google = GoogleSearch()

        

        self.search = SearchEngine()

        self.tabs = None

    def open_url(self, target):

        result = self.resolver.resolve(target)

    # --------------------------------
    # Direct Website
    # --------------------------------

        if result["type"] == "url":

            url = result["value"]

            self._update_context(
                page=None,
                site=target,
                url=url,
                title=url,
                action="open_url",
            )

            webbrowser.open(url, new=2)

            return f"Opened {url}"

    # --------------------------------
    # Official Website
    # --------------------------------

        if result["type"] == "official":

            response = self.open_official(result["value"])

            page = self.browser.current_page()

            page.wait_for_load_state("domcontentloaded")

            self._update_context(
    page=page,
    site=target,
    action="open_official",
)

            return response

    # --------------------------------
    # Google Search
    # --------------------------------

        if result["type"] == "search":

            return self.search_web(result["value"])

    # --------------------------------
    # Fallback
    # --------------------------------

        return self.search_web(target)
    def search_web(
    self,
    query,
    engine="google"
):

        url = self.search.build_search_url(
        query,
        engine
    )

        self._update_context(
            page=None,
            url=url,
            title=f"{engine} search",
            search=query,
            action="search",
        )

        webbrowser.open(url, new=2)

        return f"Searching '{query}' using {engine}"

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

    def new_tab(self):

        self.context.set_tab(
    len(self.browser.session.get_context().pages) - 1
)

        self.context.set_last_action("new_tab")

        if self.tabs is None:

            self.tabs = TabManager(
            self.browser.session.get_context()
        )

        return "New tab opened."

    def list_tabs(self):

        if self.tabs is None:

            self.browser.start()

            self.tabs = TabManager(
            self.browser.session.get_context()
        )

        return self.tabs.list_tabs()

    def switch_tab(self, index):

        if self.tabs is None:

            self.browser.start()

            self.tabs = TabManager(
        self.browser.session.get_context()
    )

        page = self.browser.current_page()

        self.context.set_tab(index)

        self._update_context(
    page=page,
    action="switch_tab",
)

        return f"Switched to tab {index}"

    def close_current_tab(self):

        if self.tabs is None:

            self.browser.start()

            self.tabs = TabManager(
        self.browser.session.get_context()
    )

        self.context.set_last_action("close_tab")

        return "Current tab closed."

    def downloader(self):

        return Downloader(
            self.browser.current_page()
        )


    def close_browser(self):

        self.browser.close()

        self.context.clear()

        return "Browser closed."
    def open_official(self, target):

        search_url = self.google.search_url(
        f"{target} official website"
    )

        self.browser.open_url(search_url)

        finder = OfficialWebsiteFinder(
        self.browser.current_page()
    )

        official = finder.find()

        if official:

            self.browser.open_url(official)

            page = self.browser.current_page()

            page.wait_for_load_state("domcontentloaded")

            self.context.set_site(target)
            self.context.set_title(page.title())

            return f"Opened official website for {target}"

        return f"Couldn't locate the official website for {target}"
    def _update_context(
        self,
    page,
    site=None,
    url=None,
    search=None,
    action=None,
    title=None,
):

        if site is not None:
            self.context.set_site(site)

        if url is None and page is not None:
            url = page.url

        if url is not None:
            self.context.set_url(url)

        if title is None and page is not None:
            title = page.title()

        if title is not None:
            self.context.set_title(title)

        if search is not None:
            self.context.set_search(search)

        if action is not None:
            self.context.set_last_action(action)

        self.context.add_history(
        url=url,
        title=title,
    )
    def current_site(self):
        return self.context.get_site()


    def current_url(self):
        return self.context.get_url()


    def current_title(self):
        return self.context.get_title()


    def current_search(self):
        return self.context.get_search()


    def current_tab(self):
        return self.context.get_tab()


    def history(self):
        return self.context.get_history()


    def last_action(self):
        return self.context.get_last_action()
