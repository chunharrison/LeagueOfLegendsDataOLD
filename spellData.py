import requests

def getSummSpellData():
	URL = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/summoner.json"
	response = requests.get(URL)
	return response.json()

summSpellData = getSummSpellData()["data"]

def getSummSpellName(spellId):
	for spell in summSpellData:
		if summSpellData[spell]["key"] == str(spellId):
			return spell
	return "non-existing spell"