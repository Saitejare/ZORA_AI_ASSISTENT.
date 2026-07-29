from pathlib import Path
from playwright.sync_api import Page, Download


class Downloader:

    def __init__(self, page: Page):
        self.page = page

    def download_from_selector(
        self,
        selector: str,
        save_dir: str = "downloads"
    ):

        save_dir = Path(save_dir)
        save_dir.mkdir(exist_ok=True)

        with self.page.expect_download() as download_info:

            self.page.locator(selector).click()

        download: Download = download_info.value

        destination = save_dir / download.suggested_filename

        download.save_as(destination)

        return str(destination)

    def download_from_url(
        self,
        url: str
    ):

        self.page.goto(url)

        return self.page.url