from requests import get as getVer


class Version:
    def __init__(self, userSettings):
        self.version = "1.1.0"
        self.new_version = ""
        if userSettings["Others"]["Check_update"]:
            self.update = self.checkVersion()
        else:
            self.update = "Check update disabled"

    def checkVersion(self):
        try:
            self.new_version = getVer("https://pastebin.com/raw/8YAjs4Pc", timeout=5).text
            return "Outdated" if self.new_version != self.version else "Up to Date"
        except Exception as e:
            return f"Cannot fetch if new update: {str(e)}"