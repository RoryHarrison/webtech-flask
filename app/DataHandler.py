import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

class DataHandler:

    def __init__(self, mdata):
        self.request = requests.get("http://ddragon.leagueoflegends.com/cdn/9.23.1/data/en_US/champion.json")
        self.mdata = mdata

    def MergeChampData(self):
        champ_data = pd.read_json(self.request.content)
        for x, mastery in enumerate(self.mdata):
            id = mastery["championId"]
            for champ in champ_data["data"]:
                if str(id) == champ["key"]:
                    self.mdata[x].update({"name":champ["name"],"codeName":champ["id"]})
        return self.mdata