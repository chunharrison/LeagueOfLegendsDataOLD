from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

from rankData import getRankData, getWinRate
from championsData import getChampName
from spellData import getSummSpellName
# from flask_run import championList, summSpellData

class Info(FlaskForm):
	summonername = StringField('Summoner Name', validators=[Length(min=3, max=25)])
	api = StringField('Retreive your API key from ')
	submit = SubmitField('Search')


# tierInfoDict: parsed dictionary from 
# 			"getRankData()"'s JSON object to 
# 			"Summoner" class ([0] for 'SOLO' and [1] for 'FLEX')
class Rank:
	def __init__(self, tierInfoDict):
		self.tier = tierInfoDict["tier"].title()		#	string
		self.tier_emblem_png = "Emblem_" + self.tier
		self.rank = tierInfoDict["rank"]				#	string
		self.points = tierInfoDict["leaguePoints"]   	#	int
		self.leagueName = tierInfoDict["leagueName"]	#	string
		self.winrate = getWinRate(tierInfoDict)			#	float
		self.wins = tierInfoDict["wins"]				#	int
		self.losses = tierInfoDict["losses"]			#	int


# summonerJSONdata: JSON object from "getSummonerData()"
# rankJSONdata: JSON object from "getRankData()"
class Summoner:
	def __init__(self, summonerJSONdata, region, api):
		# print("@@@@@@@@@@ summonerJSONdata", summonerJSONdata)
		self.iconId = summonerJSONdata["profileIconId"] #	int
		# self.iconId = str(summonerJSONdata["profileIconId"]) + ".png" # string
		self.summonername = summonerJSONdata["name"]	#	string
		self.summonerId = summonerJSONdata["id"]		#	long
		self.accountId = summonerJSONdata["accountId"]	#	long

		rankJSONdata = getRankData(region, str(self.summonerId), api)
		self.soloRankData = Rank(rankJSONdata[0]) 		#	class: Rank
		# print(self.soloRankData)
		# self.flexRankData = Rank(rankJSONdata[0])		#	class: Rank

class Player:
	def __init__(self, participantData, gameTime, summName):

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
				if itemID == 0: itemID = 3637
				items.append(itemID)
			return items

		# BASIC INFO
		self.summonerName = summName # string
		self.champion = getChampName(participantData["championId"]) # string
		# self.champion = participantData["championId"] # int
		self.level = participantData["stats"]["champLevel"] # int
		self.role = participantData["timeline"]["role"] # string
		self.lane = participantData["timeline"]["lane"] # string

		# KDA
		self.kills = participantData["stats"]["kills"] # int
		self.deaths = participantData["stats"]["deaths"] # int
		self.assists = participantData["stats"]["assists"] # int
		if float(self.deaths) <= 0:
			self.deaths = 1
		kdaFloat = (float(self.kills) + (float(self.assists) / 3)) / float(self.deaths)
		self.KDARatio = round(kdaFloat, 1) * 100

		# ITEMS AND SPELLS
		self.spell1 = getSummSpellName(participantData["spell1Id"])
		self.spell2 = getSummSpellName(participantData["spell2Id"]) 
		# self.spell1 = participantData["spell1Id"] # int
		# self.spell2 = participantData["spell2Id"] # int
		self.itemIDs = getItems(participantData["stats"])# array of ints

		# NUMERICAL DATAS
		self.creepsPMfrag = getCreepsPM(participantData["timeline"]["creepsPerMinDeltas"]) # int
		self.creepsPM = round(self.creepsPMfrag / (gameTime / 10), 1)
		self.creepsKilled = int(gameTime / self.creepsPM)
		self.creepsPM = self.creepsPM * gameTime
		self.totalDmgToChmps = participantData["stats"]["totalDamageDealtToChampions"] # int
		self.totalDmgTaken = participantData["stats"]["totalDamageTaken"] # int
		self.visionWards = participantData["stats"]["visionWardsBoughtInGame"] # int

class Team:
	# teams are array of teams (team0 and team1)
	def __init__(self, matchJSON, teamIndex):

		teamInfo = matchJSON["teams"][teamIndex]
		participants = matchJSON["participants"]
		participantIdentities = matchJSON["participantIdentities"]
		gameTime = matchJSON["gameDuration"] / 60 # floats (represents gametime in minutes)

		def getPlayers():
			players = []
			for x, participant  in enumerate(participants):
				if participant["teamId"] == self.teamID:
					summName = participantIdentities[x]["player"]["summonerName"]
					globals()["player" + str(x)] = Player(participant, gameTime, summName)
					players.append(globals()["player" + str(x)])
			return players

		self.teamID = teamInfo["teamId"]
		self.won = True  if teamInfo["win"] == "Win" else False
		self.towerKills = teamInfo["towerKills"]
		self.inhibKills = teamInfo["inhibitorKills"]
		self.dragonKills = teamInfo["dragonKills"]
		self.baronKills = teamInfo["baronKills"]
		self.riftKilled = True if teamInfo["riftHeraldKills"] == 1 else False
		self.players = getPlayers()

class Match:
	def __init__(self, matchJSON, index):
		self.index = index
		self.mode = matchJSON["gameMode"] # string
		self.duration = round(matchJSON["gameDuration"] / 60)
		self.team1 = Team(matchJSON, 0) # class
		self.team2 = Team(matchJSON, 1) # class
