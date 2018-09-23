from flask import Flask, render_template, url_for, flash, redirect
from forms import Info, Summoner, Rank
from riotApi import getSummonerData, getRankData
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

	# important IDs from SummonerData
	responseJSONSummonerData = getSummonerData(region, summonername, api)
	summoner = Summoner(responseJSONSummonerData)

	# RANK
	responseJSONRankData = getRankData(region, str(summoner.summonerID), api)
	rank = Rank(responseJSONRankData)

	return render_template('data.html', rank=rank)

if __name__ == '__main__':
	app.run(debug=True)
