from datetime import datetime


class BrowserContext:

    def __init__(self):

        self.clear()

    # --------------------------------------------------
    # Current Website
    # --------------------------------------------------

    def set_site(self, site):

        self.current_site = site

    def get_site(self):

        return self.current_site

    # --------------------------------------------------
    # Current URL
    # --------------------------------------------------

    def set_url(self, url):

        self.current_url = url

    def get_url(self):

        return self.current_url

    # --------------------------------------------------
    # Page Title
    # --------------------------------------------------

    def set_title(self, title):

        self.current_page_title = title

    def get_title(self):

        return self.current_page_title

    # --------------------------------------------------
    # Search Query
    # --------------------------------------------------

    def set_search(self, query):

        self.current_search = query

    def get_search(self):

        return self.current_search

    # --------------------------------------------------
    # Active Tab
    # --------------------------------------------------

    def set_tab(self, index):

        self.current_tab = index

    def get_tab(self):

        return self.current_tab

    # --------------------------------------------------
    # Last Action
    # --------------------------------------------------

    def set_last_action(self, action):

        self.last_action = action

    def get_last_action(self):

        return self.last_action

    # --------------------------------------------------
    # Browser History
    # --------------------------------------------------

    def add_history(
        self,
        url,
        title="",
    ):

        self.history.append(
            {
                "url": url,
                "title": title,
                "time": datetime.now(),
            }
        )

    def get_history(self):

        return self.history

    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    def clear(self):

        self.current_site = None
        self.current_url = None
        self.current_page_title = None
        self.current_search = None
        self.current_tab = 0
        self.last_action = None
        self.history = []