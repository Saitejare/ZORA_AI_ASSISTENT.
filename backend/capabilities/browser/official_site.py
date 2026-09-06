from playwright.sync_api import Page


class OfficialWebsiteFinder:

    def __init__(self, page: Page):
        self.page = page

    def find(self):

        self.page.wait_for_load_state("networkidle")

        links = self.page.locator("a")

        count = links.count()

        candidates = []

        for i in range(count):

            href = links.nth(i).get_attribute("href")

            if not href:
                continue

            href = href.strip()

            # Ignore invalid links
            if href in ("#", "/"):
                continue

            if href.startswith(("javascript:", "mailto:", "tel:")):
                continue

            if href.startswith("/"):
                continue

            if not href.startswith(("http://", "https://")):
                continue

            if "google.com" in href.lower():
                continue

            if "webcache" in href.lower():
                continue

            candidates.append(href)

        # Return the first valid external website
        if candidates:
            return candidates[0]

        return None