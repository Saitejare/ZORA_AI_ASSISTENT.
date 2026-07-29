from urllib.parse import quote_plus


class SearchEngine:

    ENGINES = {
        "google": "https://www.google.com/search?q={}",
        "youtube": "https://www.youtube.com/results?search_query={}",
        "bing": "https://www.bing.com/search?q={}",
        "duckduckgo": "https://duckduckgo.com/?q={}",
        "github": "https://github.com/search?q={}",
        "wikipedia": "https://en.wikipedia.org/wiki/Special:Search?search={}"
    }

    def build_search_url(
        self,
        query: str,
        engine: str = "google"
    ):

        engine = engine.lower()

        if engine not in self.ENGINES:
            raise ValueError(f"Unsupported search engine: {engine}")

        query = quote_plus(query)

        return self.ENGINES[engine].format(query)

    def normalize_url(self, url: str):

        url = url.strip()

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url