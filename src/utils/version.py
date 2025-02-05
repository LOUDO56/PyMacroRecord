import requests
from requests.exceptions import RequestException

class Version:
    def __init__(self, userSettings, main_app):
        self.main_app = main_app
        self.version = "1.1.9.4"
        self.new_version = ""
        if userSettings["Others"]["Check_update"]:
            self.update = self.checkVersion()
        else:
            self.update = self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["disabled"]

    def checkVersion(self):
        api_url = f'https://api.github.com/repos/LOUDO56/PyMacroRecord/releases/latest'

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                release_data = response.json()
                self.new_version = release_data['tag_name'].replace('v', '')
                return self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["outdated"] \
                    if self.new_version != self.version \
                    else self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["up_to_date"]
            else:
                return self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["failed"]
        except RequestException:
            return self.main_app.text_content["help_menu"]["about_settings"]["version_check_update_text"]["failed"]