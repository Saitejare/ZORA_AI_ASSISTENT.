from rapidfuzz import process, fuzz


class ApplicationMatcher:

    def __init__(self):
        self.threshold = 65

    def match(self, target: str, applications: dict):

        target = target.lower().strip()

        choices = list(applications.keys())

        result = process.extractOne(
            target,
            choices,
            scorer=fuzz.WRatio
        )

        if result is None:
            return None

        name, score, _ = result

        if score < self.threshold:
            return None

        return {
            "name": name,
            "path": applications[name],
            "score": score
        }