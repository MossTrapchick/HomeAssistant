import json
from datetime import datetime

class Functions:
    def __init__(self):
        self.funcs = {
            "Текущая дата": lambda: self.now("%d.%m.%Y"),
            "Текущее время": lambda: self.now("%H:%M"),
            "День недели": lambda: self.now("%A"),
        }

        with open("commands.json", "w", encoding="utf-8") as file:
            json.dump(list(self.funcs.keys()), file, ensure_ascii=False, indent=2 )

    def CheckForCommand(self, text):
        for command in self.funcs.keys():
            if(command in text):
                return self.funcs[command]()
        return None

    def now(self, fmt):
        return datetime.now().strftime(fmt)
