import time
from flask import Flask, render_template, url_for, flash, redirect

from forms import Info, Summoner
from modules.summonerData import getSummonerData
from matchData import getMatchListData, get10Matches
# from championsData import getChampionList
# from spellData import getSummSpellData

import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '17c20e187af0a720edd80183221796ae'

# @app.route("/about")
# def about():
#     return render_template('about.html') 

@app.route("/", methods=['GET', 'POST'])
def home():
	form = Info()
	if form.validate_on_submit():
		return redirect(url_for('data', summonername=str(form.summonername.data), api=str(form.api.data)))
	return render_template('homepage.html', form=form)

@app.route("/<summonername>/<api>")
def data(summonername, api):
	region = 'na1'
	# SUMMONER
	responseJSONSummonerData = getSummonerData(summonername, api)
	summoner = []
	try:
		summoner = Summoner(responseJSONSummonerData, region, api)
	except Exception as e:
		# return str(e)
		return render_template('oopsie.html')
	# summoner = ''
	# while responseJSONSummonerData.get('status', {'status_code': 200})['status_code'] == 403: 
	# 	try:
	# 		summoner = Summoner(responseJSONSummonerData, region, api)
	# 	except:
	# 		responseJSONSummonerData = getSummonerData(summonername, api)
	# summonername, summonerId, accountId, soloRankData, flexRankData)
	# print("@@@@@@@@@@ responseJSONSummonerData", responseJSONSummonerData)
	# summoner = Summoner(responseJSONSummonerData, region, api)

	# MATCHES
	# print("@@@@@@@@@@ summoner", summoner)
	responseJSONMatchListData = getMatchListData(region, str(summoner.accountId), api)
	# print("@@@@@@@@@@ responseJSONMatchListData", responseJSONMatchListData)
	matches10 = get10Matches(responseJSONMatchListData["matches"], region, api)

	return render_template('data.html', summoner=summoner, matches10=matches10)

if __name__ == '__main__':
	app.run()
