import requests
from summonerData import getSummonerData
from rankData import getRankData, getRankTier, getWinRate
from matchData import getMatchListData, getMatchData, get10Matches
from championsData import getChampionList, getChampName

## NOTE ##
# leagues service uses "summonerId"
# match service uses "accountID"

def main():

    # important IDs from SummonerData
	responseJSONSummonerData  = getSummonerData(summonername, api)
	summonerId = str(responseJSONSummonerData["id"])
	accountID = str(responseJSONSummonerData["accountId"])

    # RANK
	responseJSONRankData = getRankData(region, summonerId, api) 
	soloRank = getRankTier(responseJSONRankData, "SOLO")
	flexRank = getRankTier(responseJSONRankData, "FLEX")
	soloWR = getWinRate(responseJSONRankData, "SOLO")
	flexWR = getWinRate(responseJSONRankData, "FLEX")

	# CHAMPTIONS
	championList = getChampionList()["data"]

    # MATCH
	responseJSONMatchListData = getMatchListData(region, accountID, api)
	matches10 = get10Matches(responseJSONMatchListData["matches"], region, api)


if __name__ == "__main__":
    main()
	