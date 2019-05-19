import requests

from forms import Match

# 
def getMatchListData(region, accountId, api):
	URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + "?api_key=" + api
	response = requests.get(URL)
	return response.json()

def getMatchData(region, gameId, api):
	URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + gameId + "?api_key=" + api
	response = requests.get(URL)
	return response.json()

# list of 10 latest matches of the summoner
def get10Matches(matchlist, region, api):
	matches = []
	for x in range(1, 11):
		matchId = str(matchlist[x]["gameId"])
		responseJSONMatchData = getMatchData(region, matchId, api)
		match = Match(responseJSONMatchData, x)
		matches.append(match)
	return matches
