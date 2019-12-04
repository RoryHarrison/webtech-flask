from app import app
import json
import requests
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
def get_data():
    #Throws 400 if no args
    summoner = request.args['summoner']
    region = request.args['region']
    
    #Summoner Request
    sreq = requests.get('https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(region, summoner, Config.API_KEY))

    if sreq.status_code != 200:
        abort(sreq.status_code)
    
    #Summoner Data as Dict
    sdata = json.loads(sreq.content)
    
    #Encrypted Summoner ID
    sid=sdata["id"]

    #Mastery Request
    mreq = requests.get('https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?api_key={}'.format(region, sid, Config.API_KEY))

    if mreq.status_code != 200:
        abort(mreq.status_code)

    #Mastery Point Data as List of Dicts
    mdata = json.loads(mreq.content)

    return render_template('summoner.html', sdata=sdata, mdata=mdata)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(400)
def client_error(e):
    return render_template('404.html'), 400