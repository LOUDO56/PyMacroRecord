from threading import Thread

from requests import get
from requests.exceptions import RequestException


class Version:
    def __init__(self, userSettings, main_app):
        self.main_app = main_app
        self.version = "1.4.3"
        self.new_version = ""
        if userSettings["Others"]["Check_update"]:
            self.update = ""
            Thread(target=self._check_async, daemon=True).start()
        else:
            self.update = self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["disabled"]

    def _check_async(self):
        self.update = self.checkVersion()
        try:
            self.main_app.after(0, getattr(self.main_app, 'on_version_checked', lambda: None))
        except Exception:
            pass

    def checkVersion(self):
        api_url = 'https://api.github.com/repos/LOUDO56/PyMacroRecord/releases/latest'

        try:
            response = get(api_url, timeout=10)

            if response.status_code == 200:
                release_data = response.json()
                self.new_version = release_data.get('tag_name', '').replace('v', '')
                return (
                    self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["outdated"]
                    if self.new_version and self.new_version != self.version
                    else self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["up_to_date"]
                )
            else:
                return self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["failed"]
        except RequestException:
            return self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["failed"]

    def refresh_locale_text(self):
        """Recompute localized update text for current language without rechecking network."""
        vt = self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]
        try:
            if not self.main_app.settings.settings_dict["Others"]["Check_update"]:
                self.update = vt["disabled"]
                return
        except Exception:
            pass
        if self.new_version:
            self.update = vt["outdated"] if self.new_version != self.version else vt["up_to_date"]
        else:
            if not self.update:
                self.update = vt.get("checking", "")
            else:
                self.update = vt["failed"]
