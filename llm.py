import requests, json

OLLAMA_URL = "http://localhost:11434/api/chat"
CloudModel = "deepseek-v3.1:671b-cloud"
LocalModel = "hf.co/unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF:Q5_K_M"

class Llm:
    def __init__(self, presetPath = "preset.txt", commandsPath = "commands.json"):
        with open(presetPath, "r", encoding="utf-8") as f:
            preset = f.read()
        with open(commandsPath, 'r', encoding='utf-8') as json_file:
            commands = json.load(json_file)
        self.dialog = [{
                "role": "system",
                "content": preset + ','.join(commands)
        }]
        print(self.dialog)
    
    def has_internet(self):
        try:
            requests.get("https://chat.deepseek.com", timeout=3)
            return True
        except requests.RequestException:
            return False

    def ask_llm(self,text, role = "user"):
        self.dialog.append({"role": role, "content": text})

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": CloudModel if self.has_internet() else LocalModel,
                "messages": self.dialog,
                "stream": False
            }
        )

        reply = response.json()["message"]["content"]
        self.dialog.append({"role": "assistant", "content": reply})
        return reply