import requests
from requests.exceptions import RequestException

class Version:
    def __init__(self, userSettings):
        self.version = "1.1.12"
        self.new_version = ""
        if userSettings["Others"]["Check_update"]:
            self.update = self.checkVersion()
        else:
            self.update = "Check update disabled"

    def checkVersion(self):
        api_url = f'https://api.github.com/repos/LOUDO56/PyMacroRecord/releases/latest'

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                release_data = response.json()
                self.new_version = release_data['tag_name'].replace('v', '')
                return "Outdated" if self.new_version != self.version else "Up to Date"
            else:
                return "Cannot fetch if new update"
        except RequestException:
            return "Cannot fetch if new update"