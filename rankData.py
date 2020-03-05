import requests


### getRankData()
# requires "summonerId" from getSummonerData()
# returns a JSON object that contains summoner's RANKED SOLO and RANKED FLEX details
# 
# Parameters:
# requires summonerId from getSummonerData()
# 	- region: 		STRING 		| value of the summoner's region
# 	- summonerId: 	STRING 		| value of the summoner's summonerId
# 	- api:  		STRING 		| value of the user's(person who is using this program) Riot Games API key
def getRankData(region, summonerId, api):
	URL = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + summonerId + "?api_key=" + api
	response = requests.get(URL)
	return response.json()


### getWinRate()
# requires "rankData" from getRankData()
# returns a float value of summoner's winrate (rounded off the 3 decimal places)
# 
# Parameters:
# getRankData: dictionary of all the rank info
def getWinRate(rankData):
	wins = float(rankData["wins"])
	losses = float(rankData["losses"])
	winrate = wins / (wins + losses)
	winrate = round(winrate, 3)
	return winrate * 100
