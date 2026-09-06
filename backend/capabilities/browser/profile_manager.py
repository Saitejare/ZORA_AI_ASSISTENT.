from pathlib import Path
import os
import json

class ChromeProfileManager:

    def __init__(self):
        self.user_data = Path(
            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\User Data"
            )
        )
        self.config = self.user_data / "zora_profile.json"

    def profiles(self):

        profiles = []

        if not self.user_data.exists():
            return profiles

        for folder in sorted(self.user_data.iterdir()):

            if not folder.is_dir():
                continue

            if folder.name == "Default" or folder.name.startswith("Profile"):

                profiles.append(
                {
                    "id": folder.name,
                    "name": self.profile_name(folder),
                    "path": str(folder),
                }
            )

        return profiles

    def profile_name(self, folder: Path):

        preferences = folder / "Preferences"

        if preferences.exists():

            try:

                import json

                with open(
                    preferences,
                    encoding="utf-8",
                ) as f:

                    data = json.load(f)

                return data["profile"]["name"]

            except Exception:
                pass

        return folder.name
    def get_profile(self, profile_id):

        for profile in self.profiles():

            if (
                profile["id"].lower() == profile_id.lower()
                or profile["name"].lower() == profile_id.lower()
            ):
                return profile

        return None
    def save_last_profile(self, profile_id):

        with open(self.config, "w") as f:

            json.dump({
                "last_profile": profile_id},f,indent=4,)


    def last_profile(self):

        if not self.config.exists():
            return None

        with open(self.config) as f:

            return json.load(f).get("last_profile")
