import random
import os
import json
import requests

def get_random_user():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    user_agents_file = f"{package_directory}/tmp/user-agents.json"
    os.makedirs(os.path.dirname(user_agents_file), exist_ok=True)
    def load_useragents():
        if not os.path.exists(user_agents_file):
            r = requests.get("https://raw.githubusercontent.com/opawg/user-agents/master/src/user-agents.json")
            with open(user_agents_file, "w") as f:
                f.write(r.text)

        with open(user_agents_file) as f:
            json_file = json.load(f)
        return json_file
    
    user_agents = load_useragents()
    while True:
        user = random.choice(user_agents)
        try:
            return random.choice(user["examples"])
        except:
            continue