import requests

### getChampionList()
# Returns a JSON object that contains static data of every champions in the game
def getChampionList():
	URL = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
	response = requests.get(URL)
	return response.json()

champList = getChampionList()["data"]

### getChampName()
# Returns the name of the champion that corresponds to the given "champId" by
# iterating through "champList" retreived from "getChampionList()"
def getChampName(champId):
	for name in champList:
		if champList[name]["key"] == str(champId):
			return name
	return "non-existing champion"