class BrowserSessionManager:

    def __init__(self):

        self.context = None
        self.page = None

    # -------------------------

    def set_context(self, context):

        self.context = context

    # -------------------------

    def get_context(self):

        return self.context

    # -------------------------

    def has_context(self):

        return self.context is not None

    # -------------------------

    def set_page(self, page):

        self.page = page

    # -------------------------

    def get_page(self):

        return self.page

    # -------------------------

    def has_page(self):

        return (
            self.page is not None
            and not self.page.is_closed()
        )

    # -------------------------

    def clear(self):

        self.context = None
        self.page = None