import json, webbrowser, re
from datetime import datetime

class Functions:
    def __init__(self):
        self.funcs = {
            "Current Date": lambda text: self.now("%d.%m.%Y"),
            "Current Time": lambda text: self.now("%H:%M"),
            "Day Of Week": lambda text: self.now("%A"),
            "OpenUrl *url*": lambda text: self.OpenUrl(text),
        }

        with open("commands.json", "w", encoding="utf-8") as file:
            json.dump(list(self.funcs.keys()), file, ensure_ascii=False, indent=2 )

    def CheckForCommand(self, text):
        for command in self.funcs.keys():
            prefix = command.split("*")[0].strip()
            if(prefix in text):
                return self.funcs[command](text)
        return None

    def now(self, fmt):
        return datetime.now().strftime(fmt)
    def OpenUrl(self, text):
        match = re.search(r'https?://[^\s"<>]+', text)
        if not match:
            return "Ссылка не найдена"
        webbrowser.open(match.group(0), new=0)
        return "Opened"