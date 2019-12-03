from app import app
import json
import requests
from forms import SummonerForm
from flask import Flask, render_template, redirect, request, make_response

@app.route('/')
@app.route('/index')
def index():
    form = SummonerForm()
    return render_template('index.html', form=form)

@app.route('/summoner', methods=['GET', 'POST'])
def get_data():
    #Throws 400 if no args
    summoner = request.args['summoner']
    region = request.args['region']

    data = json.loads(requests.get('https://www.masterypoints.com/api/v1.1/summoner/{}/{}'.format(summoner, region)).content)

    return render_template('summoner.html', data=data)

    