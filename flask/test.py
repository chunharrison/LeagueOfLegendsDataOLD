import requests

# class MPlayer:
# 	def __init__(self, summName, champion, kills, deaths, assists, 
# 		level, items, creepPM, totalDmgToChmps, totalDmgTaken, visionWards):
# 		self.summName = summName; # string
# 		self.champion = champion; # string/int
# 		self.kills = kills; # int
# 		self.deaths = deaths; # int
# 		self.assists = assists; # int
# 		self.level = level; # int
# 		self.items = items; # array of strings
# 		self.creepPM = creepPM; # int
# 		self.totalDmgToChmps = totalDmgToChmps; # int
# 		self.totalDmgTaken = totalDmgTaken; # int
# 		self.visionWards = visionWards; # int


# class Match:
# 	def __int__(self, gametype, team1Won, team2Won, players):
# 		self.gametype = gametype # string
# 		self.team1 = team1 # boolean
# 		self.team1 = team1 # boolean
# 		self.players = players # array of class


# def getSummonerData(region, summonerName, APIKey):
#     URL = 'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + APIKey
#     # print(URL)
#     response = requests.get(URL)
#     return response.json()

# # requires summonerID from getSummonerData
# # data about RANKED SOLO and RANKED FLEX
# def getRankData(region, summonerID, APIKey):
# 	URL = 'https://' + region + '.api.riotgames.com/lol/league/v3/positions/by-summoner/' + summonerID + '?api_key=' + APIKey
# 	response = requests.get(URL)
# 	return response.json()

# # getRankData: json dictionary of all the rank info
# # type: string value of either 'SOLO' or 'FLEX'
# # returns a string value of summoner's rank tier
# def getRankTier(rankData, type):
# 	index = 0 if type == 'SOLO' else 1 
# 	tier = rankData[index]['tier']
# 	rank = rankData[index]['rank']
# 	leagueName = rankData[index]['leagueName']
# 	RankSummary = tier + ' ' + rank + " in " + leagueName
# 	return RankSummary

# # getRankData: json dictionary of all the rank info
# # type: string value of either 'SOLO' or 'FLEX'
# # returns a float value of summoner's winrate
# def getWinRate(rankData, type):
# 	index = 0 if type == 'SOLO' else 1
# 	wins = str(rankData[index]['wins'])
# 	losses = str(rankData[index]['losses'])
# 	winrate = float(wins) / ( float(wins) + float(losses))
# 	winrate = round(winrate, 3)
# 	return winrate

# # returns a JSON list of all the matches 
# def getMatchListData(region, accountID, APIKey):
# 	URL = "https://" + region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + accountID + '?api_key=' + APIKey
# 	response = request.get(URL)
# 	return response

# def getMatchData(region, gameID, APIKey):
# 	URL = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + gameID + '?api_key=' + APIKey
# 	response = request.get(URL)
# 	return response

# def getChampionList():
# 	URL = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
# 	response = requests.get(URL)
# 	return response.json()

# def getChampName(champList, champID):
# 	for name in champList:
# 		if champList[name]['key'] == str(champID):
# 			return name

# 	return "non-existing champion"
def getMatchListData(region, accountID, api):
	URL = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + accountID + '?api_key=' + api
	response = requests.get(URL)
	return response.json()

def main():
	region = 'na1'
	summonerName = '980409'
	APIKey = 'RGAPI-41cb30d5-3c52-4798-958a-b9ff1c40dba5'

 #    # important IDs from SummonerData
	# responseJSONSummonerData  = getSummonerData(region, summonerName, APIKey)
	# # print ('\n responseJSONSummonerData: ' + str(responseJSONSummonerData) + '\n')
	# summonerID = str(responseJSONSummonerData['id'])
	# # print ('\n summonerID: ' + summonerID + '\n')
	# accountID = str(responseJSONSummonerData['accountId'])
	# # print ('\n accountID: ' + accountID + '\n')

	# # RANK
	# responseJSONRankData = getRankData(region, summonerID, APIKey) 
	# rankTierSolo = getRankTier(responseJSONRankData, 'SOLO')
	# # print(rankTierSolo)
	# winRateSolo = getWinRate(responseJSONRankData, 'SOLO')
	# # print(winRateSolo)
	# rankTierFlex = getRankTier(responseJSONRankData, 'FLEX')
	# # print(rankTierFlex)
	# winRateFlex = getWinRate(responseJSONRankData, 'FLEX')
	# # print(winRateFlex)


	# # MATCH
	# responseJSONMatchData = getMatchListData(region, accountID, APIKey)
	# champl = getChampionList()
	# champ = getChampName(champl['data'], 27)
	# print(champ)

	responseJSONMatchListData = getMatchListData(region, '40433572', APIKey)
	print responseJSONMatchListData





if __name__ == "__main__":
    main()

