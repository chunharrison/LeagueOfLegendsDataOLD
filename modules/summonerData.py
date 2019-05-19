import requests


### getSummonerData()
# Returns a JSON object that contains information about the summoner
# 
# Parameters
# 	- region: 			STRING 	| value of the summoner's region. (JUST USING NA FOR NOW)
# 	- summonername: 	STRING	| value of the summoner's summonername.
# 	- api: 				STRING 	| value of the user's(person who is using this program) Riot Games API key.
# 
# JSON documentation
# 	- profileIconId: 	INT 	| ID of the summoner icon associated with the summoner. 
# 	- name: 			STRING 	| Summoner name. 
# 	- summonerLevel: 	LONG 	| Summoner level associated with the summoner. 
# 	- revisionDate: 	LONG 	| Date summoner was last modified specified as epoch milliseconds.
# 									The following events will update this timestamp: profile icon change, 
# 									playing the tutorial or advanced tutorial, finishing a game, summoner name change 
# 	- id: 				LONG 	| Summoner ID. 
# 	- accountId: 		LONG 	| Account ID.
def getSummonerData(summonername, api):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonername + "?api_key=" + api
    response = requests.get(URL)
    return response.json()
