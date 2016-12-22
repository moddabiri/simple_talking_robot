import json

class State:
    def __init__(self):
        self.internet = False
        self.human_name = "human"
        self.cpu_temp = 0.0
        self.mood = "normal"
        self.ip=""
        self.buddy_ip=""

    internet = False
    human_name = "human"
    cpu_temp = 0.0
    mood = "normal"
    ip = ""
    buddy_ip = ""

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def from_JSON(self, json_data):
        def object_decoder(obj):
            self.internet = obj['internet']
            self.human_name = obj['human_name']
            self.cpu_temp = obj['cpu_temp']
            self.mood = obj['mood']
            self.ip = obj['ip']
            self.buddy_ip = obj['buddy_ip']

        data = json.loads(json_data, object_hook=object_decoder)
        