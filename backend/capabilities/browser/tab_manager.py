from playwright.sync_api import BrowserContext


class TabManager:

    def __init__(self, context: BrowserContext):
        self.context = context

    def new_tab(self):

        page = self.context.new_page()

        page.bring_to_front()

        return page


    def list_tabs(self):

        tabs = []

        for index, page in enumerate(self.context.pages):

            try:

                tabs.append(
                    {
                        "index": index,
                        "title": page.title(),
                        "url": page.url
                    }
                )

            except Exception:

                tabs.append(
                    {
                        "index": index,
                        "title": "Unknown",
                        "url": page.url
                    }
                )

        return tabs

    def current_tab(self):

        if not self.context.pages:
            return None

        return self.context.pages[-1]

    def switch_tab(self, index: int):

        pages = self.context.pages

        if index < 0 or index >= len(pages):
            raise IndexError("Tab index out of range.")

        page = pages[index]

        page.bring_to_front()

        return page

    def close_current_tab(self):

        page = self.current_tab()

        if page is None:
            return False

        page.close()

        return True

    def tab_count(self):

        return len(self.context.pages)