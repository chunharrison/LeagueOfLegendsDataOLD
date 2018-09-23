from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length
from riotApi import getRankTier, getWinRate

class Info(FlaskForm):
	summonername = StringField('Summoner Name', validators=[Length(min=3, max=25)])
	region = StringField('Region ("na1" for now)')
	api = StringField('Retreive your API key from ')
	submit = SubmitField('Search')

class Summoner:
	def __init__(self, JSONdata):
		self.summonerID = JSONdata["id"]
		self.accountID = JSONdata["accountId"]

class Rank:
	def __init__(self, JSONdata):
		self.rankTierSolo = getRankTier(JSONdata, "SOLO")
		self.winRateSolo = getWinRate(JSONdata, "SOLO")
		self.rankTierFlex = getRankTier(JSONdata, "FLEX")
		self.winRateFlex = getWinRate(JSONdata, "FLEX")