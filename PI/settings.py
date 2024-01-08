import json


def load_settings(filePath='settingsPI1.json'):
    with open(filePath, 'r') as f:
        return json.load(f)