import re


class WebsiteResolver:

    def __init__(self):

        # Only keep websites that require a specific URL.
        # Everything else will be treated as an official website request.
        self.known_sites = {
            "gmail": "https://mail.google.com",
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
        }

    def looks_like_url(self, text: str) -> bool:

        pattern = r"^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$"

        return re.match(pattern, text.strip(), re.IGNORECASE) is not None

    def resolve(self, text: str):

        original = text.strip()
        cleaned = original.lower()

        # Direct URL
        if self.looks_like_url(original):

            if not original.startswith(("http://", "https://")):
                original = "https://" + original

            return {
                "type": "url",
                "value": original
            }

        # Known services
        if cleaned in self.known_sites:

            return {
                "type": "url",
                "value": self.known_sites[cleaned]
            }

        # Everything else is treated as an official website request
        return {
            "type": "official",
            "value": original
        }