from playwright.sync_api import Page


class PageReader:

    def __init__(self, page: Page):
        self.page = page

    def title(self):
        return self.page.title()

    def url(self):
        return self.page.url

    def html(self):
        return self.page.content()

    def text(self):

        body = self.page.locator("body")

        return body.inner_text()

    def links(self):

        links = self.page.locator("a").evaluate_all(
            """
            elements => elements.map(e => ({
                text: e.innerText,
                href: e.href
            }))
            """
        )

        return links

    def images(self):

        images = self.page.locator("img").evaluate_all(
            """
            elements => elements.map(e => ({
                src: e.src,
                alt: e.alt
            }))
            """
        )

        return images

    def metadata(self):

        return {
            "title": self.title(),
            "url": self.url(),
            "text_length": len(self.text()),
            "links": len(self.links()),
            "images": len(self.images())
        }