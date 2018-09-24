import requests

## NOTE ##
# leagues service uses "summonerID"
# match service uses "accountID"

def getChampionList():
	URL = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
	response = requests.get(URL)
	return response.json()

champList = getChampionList()['data']

def getChampName(champID):
	for name in champList:
		if champList[name]["key"] == str(champID):
			return name
	return "non-existing champion"


class Player:
	def __init__(self, participantData, summName):

		def getCreepsPM(creepsPMDelta):
			totalCreepsfragged = 0 
			for timestamp in creepsPMDelta:
				totalCreepsfragged += creepsPMDelta[timestamp]
			return totalCreepsfragged

		def getItems(dataStats):
			items = []
			for x in range(7):
				item = ("item" + str(x))
				itemID = dataStats.get(item)
				items.append(itemID)
			return items

		self.summonerName = summName # string
		self.role = participantData["timeline"]["role"] # string
		self.lane = participantData["timeline"]["lane"] # string
		self.champion = getChampName(participantData["championId"]) # string
		# self.championID = participantData["championId"]
		self.kills = participantData["stats"]["kills"] # int
		self.deaths = participantData["stats"]["deaths"] # int
		self.assists = participantData["stats"]["assists"] # int
		self.level = participantData["stats"]["champLevel"] # int
		self.itemIDs = getItems(participantData["stats"])# array of ints
		self.creepsPMfrag = getCreepsPM(participantData["timeline"]["creepsPerMinDeltas"]) # int
		self.totalDmgToChmps = participantData["stats"]["totalDamageDealtToChampions"] # int
		self.totalDmgTaken = participantData["stats"]["totalDamageTaken"] # int
		self.visionWards = participantData["stats"]["visionWardsBoughtInGame"] # int

class Team:
	# teams are array of teams (team0 and team1)
	def __init__(self, teamInfo, participants, participantIdentities):

		def getPlayers():
			players = []
			for x, participant  in enumerate(participants):
				if participant["teamId"] == self.teamID:
					summname = participantIdentities[x]["player"]["summonerName"]
					globals()["player" + str(x)] = Player(participant, summname)
					players.append(globals()["player" + str(x)])
			return players

		self.teamID = teamInfo["teamId"]
		self.won = True  if teamInfo["win"] == "Win" else False
		self.towerKills = teamInfo["towerKills"]
		self.dragonKills = teamInfo["dragonKills"]
		self.baronKills = teamInfo["baronKills"]
		self.riftKilled = True if teamInfo["riftHeraldKills"] == 1 else False
		self.players = getPlayers()

class Match:
	def __init__(self, matchJSON):
		self.mode = matchJSON["gameMode"] # string
		self.duration = round(matchJSON["gameDuration"] / 60)
		self.team1 = Team(matchJSON["teams"][0], 
			matchJSON["participants"], matchJSON["participantIdentities"]) # class
		self.team2 = Team(matchJSON["teams"][1], 
			matchJSON["participants"], matchJSON["participantIdentities"]) # class


def getSummonerData(region, summonerName, api):
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + api
    response = requests.get(URL)
    return response.json()
    return region

############################################################ RANK ############################################################

# requires summonerID from getSummonerData
# returns a JSON value of RANKED SOLO and RANKED FLEX details
def getRankData(region, summonerID, api):
	URL = "https://" + region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + summonerID + "?api_key=" + api
	response = requests.get(URL)
	return response.json()


# returns a string value of summoner"s rank tier
# 	PARAMETER VARIABLES
# getRankData: json dictionary of all the rank info
# type: string value of either "SOLO" or "FLEX"]
def getRankTier(rankData, type):
	index = 0 if type == "SOLO" else 1 
	tier = rankData[index]["tier"]
	rank = rankData[index]["rank"]
	leagueName = rankData[index]["leagueName"]
	RankSummary = tier + " " + rank + " in " + leagueName
	return RankSummary


# returns a float value of summoner"s winrate (rounded off the 3 decimal places)
# 	PARAMETER VARIABLES
# getRankData: json dictionary of all the rank info
# type: string value of either "SOLO" or "FLEX"
def getWinRate(rankData, type):
	index = 0 if type == "SOLO" else 1
	wins = str(rankData[index]["wins"])
	losses = str(rankData[index]["losses"])
	winrate = float(wins) / ( float(wins) + float(losses))
	winrate = round(winrate, 3)
	return winrate

############################################################ RANK ############################################################

########################################################### MATCHES ###########################################################

# 
def getMatchListData(region, accountID, api):
	URL = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + accountID + "?api_key=" + api
	response = requests.get(URL)
	return response.json()

def getMatchData(region, gameID, api):
	URL = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + gameID + "?api_key=" + api
	response = requests.get(URL)
	return response.json()

# list of 10 latest matches of the summoner
def get10Matches(matchlist, region, api):
	matches = []
	for x in range(10):
		matchID = str(matchlist[x]["gameId"])
		responseJSONMatchData = getMatchData(region, matchID, api)
		match = Match(responseJSONMatchData)
		matches.append(match)
	return matches
 		
			 	


########################################################### MATCHES ###########################################################
########################################################### CHAMPIONS ###########################################################

def getChampionList():
	URL = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
	response = requests.get(URL)
	return response.json()

def getChampName(champID):
	champList = getChampionList()['data']
	for name in champList:
		if champList[name]["key"] == str(champID):
			return name
	return "non-existing champion"


########################################################### CHAMPTIONS ###########################################################


def main():

	# region = 'na1'
	# summonerName = '980409'
	# APIKey = 'RGAPI-d41c2cdc-bf97-410b-b311-715f2e1e1297'

	champList = getChampionList()

    # important IDs from SummonerData
	responseJSONSummonerData  = getSummonerData(region, summonerName, APIKey)
	# print ("\n responseJSONSummonerData: " + str(responseJSONSummonerData) + "\n")
	summonerID = str(responseJSONSummonerData["id"]) ## used for 
	# print ("\n summonerID: " + summonerID + "\n")
	accountID = str(responseJSONSummonerData["accountId"])
	# print ("\n accountID: " + accountID + "\n")

    # RANK
	responseJSONRankData = getRankData(region, summonerID, APIKey) 
	rankTierSolo = getRankTier(responseJSONRankData, "SOLO")
	# print(rankTierSolo)
	winRateSolo = getWinRate(responseJSONRankData, "SOLO")
	# print(winRateSolo)
	rankTierFlex = getRankTier(responseJSONRankData, "FLEX")
	# print(rankTierFlex)
	winRateFlex = getWinRate(responseJSONRankData, "FLEX")
	# print(winRateFlex)

	# CHAMPTIONS
	championList = getChampionList()["data"]

    # MATCH
	responseJSONMatchListData = getMatchListData(region, accountID, APIKey)
	matches10 = get10Matches(responseJSONMatchListData["matches"], region, APIKey)
	"""
	mathes10 //array of classes: Match:
			-self.mode = matchJSON["gameMode"] # string
			-self.duration = round(matchJSON["gameDuration"] / 60)
			-team1 //Class -> Team
				-self.teamID = teamInfo["teamId"]
				-self.won = True  if teamInfo["win"] == "Win" else False
				-self.towerKills = teamInfo["towerKills"]
				-self.dragonKills = teamInfo["dragonKills"]
				-self.baronKills = teamInfo["baronKills"]
				-self.riftKilled = True if teamInfo["riftHeraldKills"] == 1 else False
				-self.players = getPlayers() // list of classes: Player
					-player:  //Class -> Player:
						self.summonerName = summName # string
						self.role = participantData["timeline"]["role"] # string
						self.lane = participantData["timeline"]["lane"] # string
						self.champion = getChampName(participantData["championId"]) # string
						self.championID = participantData["championId"]
						self.kills = participantData["stats"]["kills"] # int
						self.deaths = participantData["stats"]["deaths"] # int
						self.assists = participantData["stats"]["assists"] # int
						self.level = participantData["stats"]["champLevel"] # int
						self.itemIDs = getItems(participantData["stats"])# array of ints
						self.creepsPMfrag = getCreepsPM(participantData["timeline"]["creepsPerMinDeltas"]) # int
						self.totalDmgToChmps = participantData["stats"]["totalDamageDealtToChampions"] # int
						self.totalDmgTaken = participantData["stats"]["totalDamageTaken"] # int
						self.visionWards = participantData["stats"]["visionWardsBoughtInGame"] # int
			-team2 //Class -> Team

	"""
	first = matches10[0]
	print first.mode
	print first.duration
	print first.team1.teamID
	print first.team1.won
	print first.team1.towerKills
	print first.team1.dragonKills
	print first.team1.baronKills
	print first.team1.riftKilled
	print first.team1.players[0].summonerName
	print first.team1.players[0].role
	print first.team1.players[0].lane
	print first.team1.players[0].champion
	# print first.team1.players[0].championID
	print first.team1.players[0].kills
	print first.team1.players[0].deaths
	print first.team1.players[0].assists
	print first.team1.players[0].level
	print first.team1.players[0].itemIDs
	print first.team1.players[0].creepsPMfrag
	print first.team1.players[0].totalDmgToChmps
	print first.team1.players[0].totalDmgTaken
	print first.team1.players[0].visionWards





if __name__ == "__main__":
    main()