from .actions import BrowserActions


class BrowserService:
    """
    Browser capability service.

    Supported actions:
        - open_url
        - search
        - new_tab
        - list_tabs
        - switch_tab
        - close_tab
        - title
        - metadata
        - text
        - close
    """

    def __init__(self):

        self.browser = BrowserActions()

        self.actions = {
            "open_url": self.open_url,
            "search": self.search,
            "new_tab": self.new_tab,
            "list_tabs": self.list_tabs,
            "switch_tab": self.switch_tab,
            "close_tab": self.close_tab,
            "title": self.title,
            "metadata": self.metadata,
            "text": self.text,
            "close": self.close,
        }

    def execute(self, action, parameters):

        handler = self.actions.get(action)

        if handler is None:
            raise Exception(f"Unsupported browser action: {action}")

        return handler(parameters)

    # ----------------------------------------------------

    def open_url(self, parameters):

        url = parameters["url"]

        return self.browser.open_url(url)

    # ----------------------------------------------------

    def search(self, parameters):

        query = parameters["query"]

        engine = parameters.get(
            "engine",
            "duckduckgo"
        )

        return self.browser.search_web(
            query,
            engine
        )

    # ----------------------------------------------------

    def new_tab(self, parameters):

        return self.browser.new_tab()

    # ----------------------------------------------------

    def list_tabs(self, parameters):

        return self.browser.list_tabs()

    # ----------------------------------------------------

    def switch_tab(self, parameters):

        index = parameters["index"]

        return self.browser.switch_tab(index)

    # ----------------------------------------------------

    def close_tab(self, parameters):

        return self.browser.close_current_tab()

    # ----------------------------------------------------

    def title(self, parameters):

        return self.browser.page_title()

    # ----------------------------------------------------

    def metadata(self, parameters):

        return self.browser.page_metadata()

    # ----------------------------------------------------

    def text(self, parameters):

        return self.browser.page_text()

    # ----------------------------------------------------

    def close(self, parameters):

        return self.browser.close_browser()