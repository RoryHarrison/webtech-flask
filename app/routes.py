from app import app
import os
import json
import requests
import pandas as pd
from DataHandler import DataHandler
from config import Config
from forms import SummonerForm
from flask import Flask, render_template, redirect, request, make_response, url_for, abort

@app.route('/')
@app.route('/index', methods=["GET","POST"])
def index():
    form = SummonerForm()
    if form.validate_on_submit():
        return redirect("/summoner?summoner={}&region={}".format(form.summoner.data, form.region.data))
    return render_template('index.html', form=form)

@app.route('/summoner', methods=['GET', 'POST'])
def summoner():
    #Throws 400 if no args
    summoner = request.args['summoner']
    region = request.args['region']
    
    #Summoner Request
    sreq = requests.get('https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(region, summoner, Config.API_KEY))
    if sreq.status_code != 200:
        abort(sreq.status_code)
    #Summoner Data as Dict
    sdata = json.loads(sreq.content)


    #Encrypted Summoner ID & Mastery Request
    sid=sdata["id"]
    mreq = requests.get('https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?api_key={}'.format(region, sid, Config.API_KEY))
    if mreq.status_code != 200:
        abort(mreq.status_code)

    #Mastery Point Data as List of Dicts
    mdata = json.loads(mreq.content)

    data_handler = DataHandler(mdata)
    #Merge champion names from a separate api call with mdata (See Report)
    mdata = data_handler.MergeChampData()

    return render_template('summoner.html', sdata=sdata, mdata=mdata)

@app.route('/highscores', methods=['GET', 'POST'])
def highscores():
    
    #ChampionData
    cdata = pd.read_json(requests.get("http://ddragon.leagueoflegends.com/cdn/9.23.1/data/en_US/champion.json").content)
    
    champion = request.args.get("champion")

    if champion is not None:
        for champ in cdata["data"]:
            if champ["name"] == champion:
                hs_data = json.loads(requests.get("https://www.masterypoints.com/api/v1.1/highscores/champion/{}/0/30/any".format(champ["key"])).content)
                return render_template("highscores.html", champ=cdata["data"], hs_data=hs_data)
        abort(404)
    return "neet :("





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(400)
def client_error(e):
    return render_template('404.html'), 400