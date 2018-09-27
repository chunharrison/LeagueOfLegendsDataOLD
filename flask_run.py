import time
from flask import Flask, render_template, url_for, flash, redirect

from forms import Info, Summoner
from summonerData import getSummonerData
from matchData import getMatchListData, get10Matches
# from championsData import getChampionList
# from spellData import getSummSpellData

import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '17c20e187af0a720edd80183221796ae'

@app.route("/")
def home():
	return render_template('homepage.html')

@app.route("/about")
def about():
    return render_template('about.html') 


@app.route("/informationrequired", methods=['GET', 'POST'])
def info():
	form = Info()
	if form.validate_on_submit():
		return redirect(url_for('data', region=str(form.region.data), 
			summonername=str(form.summonername.data), api=str(form.api.data)))
	return render_template('summonerInfo.html', form=form)

@app.route("/data/<region>/<summonername>/<api>")
def data(region, summonername, api):

	# SUMMONER
	responseJSONSummonerData = getSummonerData(region, summonername, api)
	# summonername, summonerId, accountId, soloRankData, flexRankData)
	summoner = Summoner(responseJSONSummonerData, region, api)

	# MATCHES
	responseJSONMatchListData = getMatchListData(region, str(summoner.accountId), api)
	matches10 = get10Matches(responseJSONMatchListData["matches"], region, api)

	return render_template('data.html', summoner=summoner, matches10=matches10)

if __name__ == '__main__':
	app.run(debug=True)
